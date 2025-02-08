from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import json
from Sensors.models import SensorData, ESP32Device
from decouple import config
from datetime import datetime, timedelta
import signal
import sys

BASE_NODE_SENSOR_DATA_TOPIC = "agri_space/sensors/data"
DEVICE_REGISTER_TOPIC = "agri_space/device/register"
SENSOR_CONNECTIONS_TOPIC = "agri_space/sensors/connections"

class Command(BaseCommand):
    help = 'Starts the MQTT client listener'

    def handle(self, *args, **kwargs):
        # Define the on_connect and on_message methods
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            client.subscribe(BASE_NODE_SENSOR_DATA_TOPIC)
            client.subscribe(DEVICE_REGISTER_TOPIC)

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()

                if msg.topic == DEVICE_REGISTER_TOPIC:
                    handle_device_registration(json.loads(payload))
        
                if msg.topic == BASE_NODE_SENSOR_DATA_TOPIC:
                    if payload:
                        handle_base_node_sensor_data(json.loads(payload))
                    else:
                        print(f"Received empty payload on {msg.topic}")

            except Exception as e:
                print(f"Error processing message from {msg.topic}: {e}")
        
        def handle_device_registration(payload):
            esp_device_id = payload.get("esp_device_id")
            if esp_device_id:
                print(f"Device Registered/Updated: {esp_device_id}")
                ESP32Device.objects.update_or_create(
                    esp_device_id=esp_device_id,
                    defaults={
                        "esp_device_status": True, 
                        "last_updated_at": datetime.now(),  
                    }
                )


        def handle_base_node_sensor_data(payload):
            try:
                sensor = SensorData.objects.create(
                    esp_device_id=ESP32Device.objects.get(esp_device_id=payload.get('esp_device_id')),
                    dht11_humidity=payload.get('dht11_humidity'),
                    dht11_temperature=payload.get('dht11_temperature'),
                    soil_moisture_raw_1=payload.get('soil_moisture_raw_1'),
                    soil_moisture_percent_1=payload.get('soil_moisture_percent_1'),
                    lux=payload.get('lux'),
                    atm_pressure=payload.get('atm_pressure'),
                    apds_ambient=payload.get('apds_ambient'), 
                    apds_red=payload.get('apds_red'),
                    apds_green=payload.get('apds_green'),
                    apds_blue=payload.get('apds_blue'),
                    mq_2_raw=payload.get('mq_2_raw'),
                    mq_2_percent=payload.get('mq_2_percent'), 
                    mq_135_raw=payload.get('mq_135_raw'), 
                    mq_135_percent=payload.get('mq_135_percent'), 
                    flow_rate=payload.get('flow_rate'),
                    flow_measurement_duration_sec=payload.get('flow_measurement_duration_sec'),
                    flow=payload.get('flow'),
                )
                sensor.save()
                print("Base Node Sensor data saved successfully.")
                    
            except Exception as e:
                print(f"Error saving base node sensor data: {e}")
                

        def signal_handler(sig, frame):
            print("Interrupt signal received. Shutting down MQTT client...")
            ESP32Device.objects.update(esp_device_status=False)
            print("All devices have been marked as disconnected.")
            client.disconnect()  
            client.loop_stop()  
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        MQTT_BROKER = config('MQTT_BROKER')
        client.connect(MQTT_BROKER, 1883, 60)

        client.loop_forever()