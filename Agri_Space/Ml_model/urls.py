from django.urls import path
from . import views

urlpatterns = [
    path('crop_prediction/', views.Crop_Recommendation.as_view(), name='crop_prediction'),
    path('fertilizer_prediction/', views.Fertilizer_Prediction.as_view(), name='fertilizer_prediction'),
    path('yield/', views.Yield_Prediction.as_view(), name='predict'),
    path('rgb/', views.Optimal_RGB.as_view(), name='predict_rgb'),
    path('irrigation/', views.Irrigation_Prediction.as_view(), name='predict_irrigation'),
    path('optimal-conditions/', views.OptimalCropConditionsPrediction.as_view(), name='optimal-conditions'),
]