import imaplib
import email
import re
from datetime import datetime, timedelta
from email.header import decode_header
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils.timezone import now
from decouple import config
from Sensors.models import SensorData, CropsOptimalConditions, RelayState, IrrigationCycle

class Command(BaseCommand):
    help = 'Processes replies to irrigation emails'

    def handle(self, *args, **kwargs):
        IMAP_SERVER = config('EMAIL_IMAP_SERVER')
        EMAIL_ADDRESS = config('EMAIL_HOST_USER')
        PASSWORD = config('EMAIL_HOST_PASSWORD')

        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_ADDRESS, PASSWORD)
            mail.select("inbox")

            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()

            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()

                        from_email = msg.get("From")

                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        self.process_email(body, from_email, msg)

            mail.logout()

        except Exception as e:
            self.stderr.write(f"Error: {e}")
    
    def process_email(self, body, from_email, msg):
        subject = msg.get("Subject", "").lower()
        if "re:" not in subject:
            print(f"Ignoring email without 'Re:' in subject: {subject}")
            return

        body_lower = body.lower().strip().split('\n')[0]

        print(f"Email body received: {body_lower}")

        has_stop = "stop irrigation" in body_lower
        has_start = "start irrigation" in body_lower

        if has_stop and has_start:
            self.reply_email(from_email, "Your email contains conflicting commands. Please send only one command.")
            return

        if has_stop:
            self.stop_irrigation(from_email)
            return

        if has_start:
            duration = self.extract_duration(body_lower)
            if duration:
                self.handle_case_1(duration, from_email)
            else:
                self.handle_case_2(from_email)
            return

        self.reply_email(from_email, "No valid commands were found in your email.")

    def extract_duration(self, body):
        match = re.search(r'(\d+)\s*min', body.lower())
        if match:
            return int(match.group(1))
        return None

    def handle_case_1(self, duration, from_email):
        start_time = datetime.now() + timedelta(minutes=2)
        day_of_week = start_time.strftime('%A')

        existing_cycle = IrrigationCycle.objects.filter(
            relay_state__day_of_week=day_of_week,
            start_time=start_time.time(),
            duration=timedelta(minutes=duration),
        ).exists()

        if existing_cycle:
            self.reply_email(from_email, f"Irrigation is already scheduled for {duration} minutes.")
            return

        relay_state, created = RelayState.objects.get_or_create(
            day_of_week=day_of_week,
            defaults={'state': True},
        )
        if not created:
            relay_state.state = True
            relay_state.save()

        IrrigationCycle.objects.create(
            relay_state=relay_state,
            start_time=start_time.time(),
            duration=timedelta(minutes=duration),
        )
        self.reply_email(from_email, f"Irrigation has started for {duration} minutes.")


    def handle_case_2(self, from_email):
        latest_sensor_data = SensorData.objects.last()
        if not latest_sensor_data:
            self.reply_email(from_email, "No sensor data available to determine irrigation requirements.")
            return

        crop = CropsOptimalConditions.objects.filter(crop_name="Cotton").first()
        if not crop:
            self.reply_email(from_email, "No crop-specific data found for irrigation requirements.")
            return

        optimal_soil_moisture = crop.optimal_temperature_lower_bound
        current_soil_moisture = latest_sensor_data.soil_moisture_percent_1
        if current_soil_moisture >= optimal_soil_moisture:
            self.reply_email(from_email, "Soil moisture is already at or above the optimal level. No irrigation needed.")
            return

        moisture_increase_rate = 1
        duration = int((optimal_soil_moisture - current_soil_moisture) / moisture_increase_rate)
        self.handle_case_1(duration, from_email)

    def stop_irrigation(self, from_email):
        RelayState.objects.filter(state=True).update(state=False)
        self.reply_email(from_email, "Irrigation has been stopped.")
        print(f"All active irrigation cycles have been stopped by {from_email}.")

    def reply_email(self, to_email, message):
        mail_subject = "Response from Irrigation System"
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        try:
            email.send()
            print(f"Reply sent to {to_email} with message: {message}")
        except Exception as e:
            print(f"Error sending reply: {e}")
    