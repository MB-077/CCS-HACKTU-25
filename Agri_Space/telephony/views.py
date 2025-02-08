from django.http import JsonResponse
from twilio.rest import Client
from decouple import config
from rest_framework.views import APIView

# Load credentials from environment variables
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class MakeCall(APIView):
    def post(self, request):
        try:
            to_phone = request.data.get("to")
            lang = request.data.get("lang", "en")  # Default language

            if not to_phone:
                return JsonResponse({"error": "Phone number required"}, status=400)

            responses = {
                "hi": "<Response><Say language='hi-IN'>नमस्ते! यह एग्री स्पेस का स्मार्ट सिंचाई अलर्ट है। आपके पौधे के लिए सिंचाई आवश्यक है।</Say></Response>",
                "en": "<Response><Say language='en-IN'>Hi! This is Agri Space's Smart Irrigation Alert. Irrigation Required for your plant.</Say></Response>"
            }

            call = client.calls.create(
                twiml=responses[lang],
                to=to_phone,
                from_=TWILIO_PHONE_NUMBER
            )

            return JsonResponse({"message": "Call initiated!", "call_sid": call.sid})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class SendSMS(APIView):
    def post(self, request):
        try:
            to_phone = request.data.get("to")  # Receiver's phone number
            lang = request.data.get("lang", "en")  # Default language

            messages = {
                "hi": "नमस्कार! यह संदेश एग्री स्पेस द्वारा भेजा गया है। आपकी फसल में मिट्टी की नमी अनुकूल स्तर से कम है और इसे सिंचाई की आवश्यकता है। कृपया यथाशीघ्र सिंचाई करें।",
                "en": "Hello! This message is sent by Agri Space. Your crop has less than optimal water content and requires irrigation. Please irrigate at your earliest convenience."
            }

            message = messages.get(lang, messages["en"])

            if not to_phone or not lang:
                return JsonResponse({"error": "Phone number and language are required"}, status=400)

            sms = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_phone
            )

            return JsonResponse({"message": "SMS sent!", "sms_sid": sms.sid})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
