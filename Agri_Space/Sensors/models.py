from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime
from django.utils import timezone

class ESP32Device(models.Model):
    esp_device_id = models.CharField(max_length=50, unique=True, verbose_name=_("ESP Device ID"))
    esp_device_status = models.BooleanField(default=False, verbose_name=_("ESP Device Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated At"))

    def get_status_display(self):
        return _("Connected") if self.esp_device_status else _("Disconnected")

    def __str__(self):
        return f"{self.esp_device_id} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = _("ESP32 Device")
        verbose_name_plural = _("ESP32 Devices")
        
        
class SensorData(models.Model):
    esp_device_id = models.ForeignKey(ESP32Device, on_delete=models.CASCADE, related_name='base_node_data', verbose_name=_("ESP Device ID"), db_index=True)
    dht11_humidity = models.FloatField(null=True, blank=True, verbose_name=_("DHT11 Humidity"))
    dht11_temperature = models.FloatField(null=True, blank=True, verbose_name=_("DHT11 Temperature"))
    soil_moisture_raw_1 = models.IntegerField(null=True, blank=True, verbose_name=_("Soil Moisture Raw 1"))
    soil_moisture_percent_1 = models.IntegerField(null=True, blank=True, verbose_name=_("Soil Moisture Percent 1"))
    lux = models.FloatField(null=True, blank=True, verbose_name=_("Lux Level"))
    atm_pressure = models.FloatField(null=True, blank=True, verbose_name=_("Atmospheric Pressure"))
    apds_ambient = models.IntegerField(null=True, blank=True, verbose_name=_("APDS9960 Ambient Light"))
    apds_red = models.IntegerField(null=True, blank=True, verbose_name=_("APDS9960 Red Light"))
    apds_green = models.IntegerField(null=True, blank=True, verbose_name=_("APDS9960 Green Light"))
    apds_blue = models.IntegerField(null=True, blank=True, verbose_name=_("APDS9960 Blue Light"))
    mq_2_raw = models.IntegerField(null=True, blank=True, verbose_name=_("MQ-2 Raw Value"))
    mq_2_percent = models.IntegerField(null=True, blank=True, verbose_name=_("MQ-2 Percent Value"))
    mq_135_raw = models.IntegerField(null=True, blank=True, verbose_name=_("MQ-135 Raw Value"))
    mq_135_percent = models.IntegerField(null=True, blank=True, verbose_name=_("MQ-135 Percent Value"))
    flow_rate = models.FloatField(null=True, blank=True, verbose_name=_("Flow Rate"), db_index=True)  # in liters per minute
    flow_measurement_duration_sec = models.FloatField(null=True, blank=True, verbose_name=_("Flow Measurement Duration (sec)"))
    flow = models.FloatField(null=True, blank=True, verbose_name=_("Flow")) # in liters
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_("Timestamp"), db_index=True)
    
    def timestamp_local(self):
        local_timestamp = localtime(self.timestamp)
        # Get milliseconds from microseconds
        millisec = local_timestamp.microsecond // 1000
        return local_timestamp.strftime(f"%Y-%m-%d %H:%M:%S") + f".{millisec:03d} {local_timestamp.tzname()}"
    
    def __str__(self):
        return f"{self.esp_device_id.esp_device_id} - {self.timestamp_local()}"
    
    class Meta:
        verbose_name = _("Sensor Data")
        verbose_name_plural = _("Sensor Data")