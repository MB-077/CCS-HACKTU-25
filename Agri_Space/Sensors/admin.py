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


class ChildNodeSensorDataAdmin(ModelAdmin):
    list_display = ('esp_device_id', 'child_node_id', 'timestamp', 'node_dht11_humidity', 'node_dht11_temperature', 'node_soil_moisture_percent_2', 'node_DS18B20_temperature', 'node_rain_percent',)
    list_filter = ('esp_device_id', 'child_node_id', 'timestamp',)
    search_fields = ('esp_device_id', 'child_node_id', 'timestamp',)
    ordering = ('-timestamp',)
    readonly_fields = ('esp_device_id', 'child_node_id', 'timestamp', 'node_dht11_humidity', 'node_dht11_temperature', 'node_soil_moisture_raw_2', 'node_soil_moisture_percent_2', 'node_DS18B20_temperature', 'node_rain_raw', 'node_rain_percent',)
    list_display_links = ('timestamp', 'esp_device_id', 'child_node_id',)
    list_per_page = 20
    list_max_show_all = 100
    
    fieldsets = (
        ('Node DHT11 Humidity & Temperature', {
            'fields': ('node_dht11_humidity', 'node_dht11_temperature',)
        }),
        ('Node Soil Moisture 2', {
            'fields': ('node_soil_moisture_raw_2', 'node_soil_moisture_percent_2',)
        }),
        ('Node DS18B20 Temperature', {
            'fields': ('node_DS18B20_temperature',)
        }),
        ('Node Rain Sensor', {
            'fields': ('node_rain_raw', 'node_rain_percent',)
        }),
        (None, {
            'fields': ('esp_device_id', 'child_node_id', 'timestamp', )
        }),
    )

admin.site.register(ChildNodeSensorData, ChildNodeSensorDataAdmin)


class IrrigationCycleInline(TabularInline):
    model = IrrigationCycle
    extra = 0
    
class LastIrrigationCycleInline(TabularInline):
    model = LastIrrigationCycle
    extra = 0
    readonly_fields = ('relay_state', 'irrigation_cycle', 'timestamp', )
    tab = True
    

class RelayStateAdmin(ModelAdmin):
    inlines = [IrrigationCycleInline, LastIrrigationCycleInline]
    list_display = ('day_of_week', 'state', 'last_updated')
    list_filter = ('day_of_week',)
    search_fields = ('day_of_week',)
    ordering = ('day_of_week',)
    readonly_fields = ('last_updated',)

admin.site.register(RelayState, RelayStateAdmin)   


class WaterConsumptionAdmin(ModelAdmin):
    list_display = ('flow_rate', 'irrigation_cycle', 'individual_usage', 'total_measurement_duration_sec',)
    list_filter = ('irrigation_cycle',)
    search_fields = ('flow_rate', 'irrigation_cycle',)
    readonly_fields = ('flow_rate', 'irrigation_cycle', 'individual_usage', 'total_measurement_duration_sec',)
    
admin.site.register(WaterConsumption, WaterConsumptionAdmin)


class TotalWaterUsageAdmin(ModelAdmin):
    list_display = ('total_usage',)
    readonly_fields = ('total_usage',)
    
admin.site.register(TotalWaterUsage, TotalWaterUsageAdmin)


class CropsOptimalConditionsAdmin(ModelAdmin):
    list_display = [field.name for field in CropsOptimalConditions._meta.get_fields()]
    list_filter = ('crop_name',)
    search_fields = ('crop_name', 'user',)
    ordering = ('crop_name',)
    
admin.site.register(CropsOptimalConditions, CropsOptimalConditionsAdmin)