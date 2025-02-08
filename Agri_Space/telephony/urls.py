from django.urls import path
from . import views

urlpatterns = [
    path("call/", views.MakeCall.as_view(), name="make-call"),
    path("sms/", views.SendSMS.as_view(), name="send-sms"),
]
