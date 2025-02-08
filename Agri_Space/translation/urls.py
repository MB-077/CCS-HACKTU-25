from django.urls import path
from .views import TranslateTextView

urlpatterns = [
    path('', TranslateTextView.as_view(), name='translate'),
]
