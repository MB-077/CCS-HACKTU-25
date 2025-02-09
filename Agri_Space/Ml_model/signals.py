from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from datetime import datetime
from Ml_model.models import UserCrop
from .utils import get_bbch_stage
from django.core.mail import EmailMessage, BadHeaderError
from Agri_Space.settings import EMAIL_HOST_USER
from smtplib import SMTPException
from decouple import config 
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

BBCH_FILE_PATH = "Ml_model/csv_files/crop_growth_stages_fixed_5.csv"  

@receiver(post_save, sender=UserCrop)
def notify_user_growth_stage(sender, instance, created, **kwargs):
    days_since_planting = (datetime.now().date() - instance.planting_date).days

    bbch_stage = get_bbch_stage(BBCH_FILE_PATH, instance.crop, days_since_planting)
    if bbch_stage:
        if instance.last_notified_stage != bbch_stage['Stage Code']:
            current_site = Site.objects.get_current()
            mail_subject = f"Growth Stage Update for {instance.crop}"
            message = render_to_string('Ml_model/growth_stage.html', {
                'user_name': instance.user.full_name(),
                'crop_name': instance.crop,
                'domain': current_site.domain,
                'bbch_stage': bbch_stage['Principal Stage'],
                'description': bbch_stage['Description']
            })

            to_email = config('EMAIL_HOST_USER')

            send_email = EmailMessage(
                subject=mail_subject,
                body=message,
                to=[to_email]
            )
            send_email.content_subtype = "html"

            try:
                send_email.send()
                print("Email sent for growth stage update")
            except Exception as e:
                print(f"Error sending email: {e}")

            instance.last_notified_stage = bbch_stage['Stage Code']
            instance.save()