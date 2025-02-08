from django.urls import path
from .views import make_call

urlpatterns = [
    path("call/", make_call, name="make_call"),
]
