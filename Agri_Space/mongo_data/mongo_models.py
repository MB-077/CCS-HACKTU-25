import mongoengine
from datetime import datetime

class SensorDataDoc(mongoengine.Document):
    esp_device_id = mongoengine.StringField(required=True)
    dht11_humidity = mongoengine.FloatField()
    dht11_temperature = mongoengine.FloatField()
    soil_moisture_raw_1 = mongoengine.IntField()
    soil_moisture_percent_1 = mongoengine.IntField()
    lux = mongoengine.FloatField()
    atm_pressure = mongoengine.FloatField()
    apds_ambient = mongoengine.IntField()
    apds_red = mongoengine.IntField()
    apds_green = mongoengine.IntField()
    apds_blue = mongoengine.IntField()
    mq_2_raw = mongoengine.IntField()
    mq_2_percent = mongoengine.IntField()
    mq_135_raw = mongoengine.IntField()
    mq_135_percent = mongoengine.IntField()
    flow_rate = mongoengine.FloatField()
    flow_measurement_duration_sec = mongoengine.FloatField()
    flow = mongoengine.FloatField()
    timestamp = mongoengine.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'sensor_data'  
    }


class ChildNodeSensorDataDoc(mongoengine.Document):
    esp_device_id = mongoengine.StringField(required=True)
    child_node_id = mongoengine.StringField(required=True)
    node_dht11_humidity = mongoengine.FloatField()
    node_dht11_temperature = mongoengine.FloatField()
    node_soil_moisture_raw_2 = mongoengine.IntField()
    node_soil_moisture_percent_2 = mongoengine.IntField()
    node_DS18B20_temperature = mongoengine.FloatField()
    node_rain_raw = mongoengine.IntField()
    node_rain_percent = mongoengine.IntField()
    timestamp = mongoengine.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'child_node_sensor_data'  
    }