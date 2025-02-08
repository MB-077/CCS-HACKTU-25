from django.contrib import admin

# Register your models here.
from .models import *
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline


class ESP32DeviceAdmin(ModelAdmin):
    list_display = ('esp_device_id', 'esp_device_status', 'created_at', 'last_updated_at',)
    list_filter = ('esp_device_status',)
    search_fields = ('esp_device_id',)
    ordering = ('esp_device_status',)
    readonly_fields = ('esp_device_id', 'esp_device_status', 'created_at', 'last_updated_at',)
    
admin.site.register(ESP32Device, ESP32DeviceAdmin)


class SensorDataAdmin(ModelAdmin):
    list_display = ('esp_device_id', 'timestamp', 'dht11_humidity', 'dht11_temperature', 'soil_moisture_percent_1', 'lux', 'atm_pressure', 'apds_ambient', 'apds_red', 'apds_green', 'apds_blue', 'mq_2_percent', 'mq_135_percent', 'flow_rate', 'flow_measurement_duration_sec', 'flow',)
    list_filter = ('timestamp', 'esp_device_id',)
    search_fields = ('timestamp', 'esp_device_id',)
    ordering = ('-timestamp',)
    readonly_fields = ('dht11_humidity', 'dht11_temperature', 'soil_moisture_raw_1', 'soil_moisture_percent_1', 'lux', 'atm_pressure', 'flow_rate', 'flow', 'timestamp', 'esp_device_id', 'mq_2_raw', 'mq_2_percent', 'mq_135_raw', 'mq_135_percent', 'apds_ambient', 'apds_red', 'apds_green', 'apds_blue', 'flow_measurement_duration_sec',)
    list_display_links = ('timestamp', 'esp_device_id',)
    list_per_page = 20
    list_max_show_all = 100
    
    fieldsets = (
        ('DHT11 Humidity & Temperature', {
            'fields': ('dht11_humidity', 'dht11_temperature',)
        }),
        ('Soil Moisture 1', {
            'fields': ('soil_moisture_raw_1', 'soil_moisture_percent_1',)
        }),
        ('BMP180 Atmospheric Pressure', {
            'fields': ('atm_pressure',)
        }),
        ('Flow Rate', {
            'fields': ('flow_rate', 'flow_measurement_duration_sec', 'flow',)
        }),
        ('Solar Intensity', {
            'fields': ('lux',)
        }),
        ('MQ-2 Gas Sensor', {
            'fields': ('mq_2_raw', 'mq_2_percent',)
        }),
        ('MQ-135 Gas Sensor', {
            'fields': ('mq_135_raw', 'mq_135_percent',)
        }),
        ('APDS-9960 RGB & Gesture Sensor', {
            'fields': ('apds_ambient', 'apds_red', 'apds_green', 'apds_blue',)
        }),
        (None, {
            'fields': ('esp_device_id', 'timestamp', )
        }),
    )

admin.site.register(SensorData, SensorDataAdmin)