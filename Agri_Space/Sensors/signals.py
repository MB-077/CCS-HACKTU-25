import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from .models import SensorData, WaterConsumption, RelayState, IrrigationCycle, TotalWaterUsage, CropsOptimalConditions, LastIrrigationCycle, ESP32Device, ChildNodeSensorData
from Users.models import UserStatus
from django.core.mail import EmailMessage, BadHeaderError
from Agri_Space.settings import EMAIL_HOST_USER
from smtplib import SMTPException
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from decouple import config 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.conf import settings
import pusher


@receiver(post_save, sender=SensorData)
def calculate_water_usage(sender, instance, created, **kwargs):
    if not created:
        return 

    relay_state = RelayState.objects.filter(state=True).last()
    if not relay_state:
        return

    now = datetime.now()
    today = now.strftime('%A')
    current_time = now.time()

    if relay_state.day_of_week != today:
        print("Relay state day does not match today.")
        return

    grace_period = timedelta(seconds=30)

    cycles = relay_state.cycles.all()
    for cycle in cycles:
        start_time = cycle.start_time
        scheduled_end = (datetime.combine(datetime.today(), start_time) + cycle.duration)
        cycle_start = datetime.combine(datetime.today(), start_time)
        cycle_effective_end = scheduled_end + grace_period
        
        current_dt = datetime.combine(datetime.today(), current_time)
        
        if cycle_start <= current_dt <= cycle_effective_end:
            if instance.flow_measurement_duration_sec > 0:
                average_flow_rate = (instance.flow / instance.flow_measurement_duration_sec) * 60.0
                instance.flow_rate = average_flow_rate
                instance.save(update_fields=["flow_rate"])
                
                water_consumption, wc_created = WaterConsumption.objects.get_or_create(
                    irrigation_cycle=cycle,
                    flow_rate=instance,
                    defaults={
                        'individual_usage': 0.0,
                        'total_measurement_duration_sec': 0.0,
                    }
                )
                if wc_created:
                    water_consumption.individual_usage = instance.flow
                    water_consumption.total_measurement_duration_sec = instance.flow_measurement_duration_sec
                else:
                    water_consumption.individual_usage += instance.flow
                    water_consumption.total_measurement_duration_sec += instance.flow_measurement_duration_sec
                    water_consumption.flow_rate = instance  

                water_consumption.save()

                total_water_usage, created_total = TotalWaterUsage.objects.get_or_create(id=1)
                total_water_usage.total_usage += instance.flow
                total_water_usage.save()

                print(
                    f"Processed sensor reading at {instance.timestamp}: "
                    f"Flow used: {instance.flow} L, duration: {instance.flow_measurement_duration_sec} sec, "
                    f"Avg. flow rate: {average_flow_rate:.2f} L/min"
                )
            else:
                print(f"Measurement duration missing for sensor reading at {instance.timestamp}.")
            break  
    else:
        print("No matching irrigation cycle found for today.")
         
@receiver(post_save, sender=IrrigationCycle)
def update_last_irrigation_cycle(sender, instance, created, **kwargs):
    if created:
        LastIrrigationCycle.objects.update_or_create(
            relay_state=instance.relay_state,
            defaults={'irrigation_cycle': instance}
        )
        
@receiver(post_save, sender=ESP32Device)
def log_device_status_change(sender, instance, created, **kwargs):
    if created:
        description = f"New device registered: {instance.esp_device_id}."
    else:
        status = "Connected" if instance.esp_device_status else "Disconnected"
        description = f"Device {instance.esp_device_id} status updated to {status}."
        

pusher_client = pusher.Pusher(
    app_id=config('PUSHER_APP_ID'),
    key=config('PUSHER_KEY'),
    secret=config('PUSHER_SECRET'),
    cluster=config('PUSHER_CLUSTER'),
    ssl=True
)

def broadcast_sensor_update(instance):
    channel_name = f"sensor-{instance.esp_device_id.esp_device_id}"
    event_name = "sensor-update"
    
    if isinstance(instance, SensorData):
        payload = {
            "dht11_temperature": instance.dht11_temperature,
            "dht11_humidity": instance.dht11_humidity,
            "soil_moisture_percent_1": instance.soil_moisture_percent_1,
            "lux": instance.lux,
            "atm_pressure": instance.atm_pressure,
            "apds_ambient": instance.apds_ambient,
            "apds_red": instance.apds_red,
            "apds_green": instance.apds_green,
            "apds_blue": instance.apds_blue,
            "mq_2_percent": instance.mq_2_percent,
            "mq_135_percent": instance.mq_135_percent,
            "flow_rate": instance.flow_rate,
            "flow_measurement_duration_sec": instance.flow_measurement_duration_sec,
            "flow": instance.flow,
            "timestamp": instance.timestamp_local(),
        }

    elif isinstance(instance, ChildNodeSensorData):
        payload = {
            "child_node_id": instance.child_node_id,
            "node_dht11_temperature": instance.node_dht11_temperature,
            "node_dht11_humidity": instance.node_dht11_humidity,
            "node_soil_moisture_percent_2": instance.node_soil_moisture_percent_2,
            "node_DS18B20_temperature": instance.node_DS18B20_temperature,
            "node_rain_percent": instance.node_rain_percent,
            "timestamp": instance.timestamp_local(),
        }
    else:
        payload = {}

    response = pusher_client.trigger(channel_name, event_name, payload)
    return response

@receiver(post_save, sender=SensorData)
def sensor_data_post_save(sender, instance, created, **kwargs):
    broadcast_sensor_update(instance)

@receiver(post_save, sender=ChildNodeSensorData)
def child_node_sensor_data_post_save(sender, instance, created, **kwargs):
    broadcast_sensor_update(instance)