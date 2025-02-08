from django.urls import path
from . import views

urlpatterns = [
    path('crop_prediction/', views.Crop_Prediction.as_view(), name='crop_prediction'),
    path('fertilizer_prediction/', views.Fertilizer_Prediction.as_view(), name='fertilizer_prediction'),
]