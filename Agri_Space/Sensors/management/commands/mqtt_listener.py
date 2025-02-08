from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import json
from Sensors.models import SensorData, ESP32Device, RelayState, ChildNodeSensorData
from decouple import config
from datetime import datetime, timedelta
import signal
import sys
import utils.mongo_connection
from mongo_data.mongo_models import SensorDataDoc, ChildNodeSensorDataDoc

BASE_NODE_SENSOR_DATA_TOPIC = "agri_space/sensors/data"
RELAY_STATE_TOPIC = "agri_space/relay/state"
RELAY_STATE_REQUEST_TOPIC = "agri_space/relay/request"
RESET_DEVICE_TOPIC = "agri_space/device/reset"
DEVICE_REGISTER_TOPIC = "agri_space/device/register"
SENSOR_CONNECTIONS_TOPIC = "agri_space/sensors/connections"
CHILD_NODE_SENSOR_DATA_TOPIC = "agri_space/sensors/child_node_data"

class Command(BaseCommand):
    help = 'Starts the MQTT client listener'

    def handle(self, *args, **kwargs):
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            client.subscribe(BASE_NODE_SENSOR_DATA_TOPIC)
            client.subscribe(CHILD_NODE_SENSOR_DATA_TOPIC)
            client.subscribe(RELAY_STATE_REQUEST_TOPIC)
            client.subscribe(DEVICE_REGISTER_TOPIC)

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode()

                if msg.topic == DEVICE_REGISTER_TOPIC:
                    handle_device_registration(json.loads(payload))
                    
                if msg.topic == BASE_NODE_SENSOR_DATA_TOPIC:
                    if payload:
                        handle_base_node_sensor_data(json.loads(payload))
                        handle_base_node_sensor_data_mongo(json.loads(payload))
                    else:
                        print(f"Received empty payload on {msg.topic}")
                        
                if msg.topic == CHILD_NODE_SENSOR_DATA_TOPIC:
                    if payload:
                        handle_child_node_sensor_data(json.loads(payload))
                        handle_child_node_sensor_data_mongo(json.loads(payload))
                    else:
                        print(f"Received empty payload on {msg.topic}")        

                if msg.topic == RELAY_STATE_REQUEST_TOPIC:
                    if payload == "request":
                        handle_relay_request()

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
        
        def handle_relay_request():
            try:
                now = datetime.now()
                today = now.strftime('%A')
                current_time = now.time()

                relay_state = RelayState.objects.filter(day_of_week=today).last()
                if relay_state:
                    if not relay_state.state:
                        client.publish(RELAY_STATE_TOPIC, json.dumps({"relay_state": "OFF", "runtime": 0}))
                        print("Relay state OFF published due to manual override.")
                        return
                    
                    cycles = relay_state.cycles.all()
                    for cycle in cycles:
                        start_time = cycle.start_time
                        end_time = (datetime.combine(datetime.today(), start_time) + cycle.duration).time()

                        if start_time <= current_time <= end_time:
                            remaining_runtime = (datetime.combine(datetime.today(), end_time) - now).total_seconds()

                            response_data = {
                                "relay_state": "ON",
                                "start_time": start_time.strftime("%H:%M:%S"),  
                                "runtime": int(remaining_runtime),  
                            }
                            client.publish(RELAY_STATE_TOPIC, json.dumps(response_data))
                            print(f"Relay state ON published: {response_data}")
                            return

                client.publish(RELAY_STATE_TOPIC, json.dumps({"relay_state": "OFF", "runtime": 0}))
                print("Relay state OFF published.")

            except Exception as e:
                print(f"Error handling relay state request: {e}")
                
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
                
        
        def handle_base_node_sensor_data_mongo(payload):
            try:
                sensor_doc = SensorDataDoc(
                    esp_device_id=payload.get('esp_device_id'),
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
                    timestamp=datetime.utcnow(),
                )
                sensor_doc.save()
                print("Base Node Sensor data saved successfully to MongoDB.")
            except Exception as e:
                print(f"Error saving base node sensor data to MongoDB: {e}")
        
                
        def handle_child_node_sensor_data(payload):
            try:
                child_node_data = ChildNodeSensorData.objects.create(
                    esp_device_id=ESP32Device.objects.get(esp_device_id=payload.get('esp_device_id')),
                    child_node_id=payload.get('child_node_id'),
                    node_dht11_humidity=payload.get('node_dht11_humidity'),
                    node_dht11_temperature=payload.get('node_dht11_temperature'),
                    node_soil_moisture_raw_2=payload.get('node_soil_moisture_raw_2'),
                    node_soil_moisture_percent_2=payload.get('node_soil_moisture_percent_2'),
                    node_DS18B20_temperature=payload.get('node_DS18B20_temperature'),
                    node_rain_raw=payload.get('node_rain_raw'),
                    node_rain_percent=payload.get('node_rain_percent'),
                )
                child_node_data.save()
                print("Child Node Sensor Data saved successfully.")
                    
            except Exception as e:
                print(f"Error saving child node sensor data: {e}")
                
        def handle_child_node_sensor_data_mongo(payload):
            try:
                child_node_data_doc = ChildNodeSensorDataDoc(
                    esp_device_id=payload.get('esp_device_id'),
                    child_node_id=payload.get('child_node_id'),
                    node_dht11_humidity=payload.get('node_dht11_humidity'),
                    node_dht11_temperature=payload.get('node_dht11_temperature'),
                    node_soil_moisture_raw_2=payload.get('node_soil_moisture_raw_2'),
                    node_soil_moisture_percent_2=payload.get('node_soil_moisture_percent_2'),
                    node_DS18B20_temperature=payload.get('node_DS18B20_temperature'),
                    node_rain_raw=payload.get('node_rain_raw'),
                    node_rain_percent=payload.get('node_rain_percent'),
                    timestamp=datetime.utcnow(),
                )
                child_node_data_doc.save()
                print("Child Node Sensor Data saved successfully to MongoDB.")
                
            except Exception as e:
                print(f"Error saving child node sensor data to MongoDB: {e}")
                
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