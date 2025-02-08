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

            twiml_response = f'<Response><Say language="{lang}-IN">Hello, this is an automated call!</Say></Response>'

            call = client.calls.create(
                twiml=twiml_response,
                to=to_phone,
                from_=TWILIO_PHONE_NUMBER
            )

            return JsonResponse({"message": "Call initiated!", "call_sid": call.sid})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
