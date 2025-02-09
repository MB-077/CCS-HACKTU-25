from django.urls import path
from .views import SensorHumidityTempView, SensorFlowView

urlpatterns = [
    path('group_sensor_data/humidity_temperature/', SensorHumidityTempView.as_view(), name='sensor_humidity_temperature'),
    path('group_sensor_data/flow/', SensorFlowView.as_view(), name='sensor_flow'),
]