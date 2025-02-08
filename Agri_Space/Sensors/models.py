from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime
from django.utils import timezone
import datetime

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
        
        
class ChildNodeSensorData(models.Model):
    esp_device_id = models.ForeignKey(ESP32Device, on_delete=models.CASCADE, related_name='child_node_data', verbose_name=_("ESP Device ID"), db_index=True)
    child_node_id = models.CharField(max_length=50, verbose_name=_("Child Node ID"))
    node_dht11_humidity = models.FloatField(null=True, blank=True, verbose_name=_("Node Humidity"))
    node_dht11_temperature = models.FloatField(null=True, blank=True, verbose_name=_("Node Temperature"))
    node_soil_moisture_raw_2 = models.IntegerField(null=True, blank=True, verbose_name=_("Node Soil Moisture Raw 2"))
    node_soil_moisture_percent_2 = models.IntegerField(null=True, blank=True, verbose_name=_("Node Soil Moisture Percent 2"))
    node_DS18B20_temperature = models.FloatField(null=True, blank=True, verbose_name=_("Node DS18B20 Temperature"))
    node_rain_raw = models.IntegerField(null=True, blank=True, verbose_name=_("Node Rain Raw"))
    node_rain_percent = models.IntegerField(null=True, blank=True, verbose_name=_("Node Rain Percent"))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_("Timestamp"))

    def timestamp_local(self):
        local_timestamp = localtime(self.timestamp)
        # Get milliseconds from microseconds
        millisec = local_timestamp.microsecond // 1000
        return local_timestamp.strftime(f"%Y-%m-%d %H:%M:%S") + f".{millisec:03d} {local_timestamp.tzname()}"
    
    def __str__(self):
        return f"{self.esp_device_id.esp_device_id} - {self.child_node_id} - {self.timestamp_local()}"

    class Meta:
        verbose_name = _("Child Node Sensor Data")
        verbose_name_plural = _("Child Node Sensor Data")
        
    
class RelayState(models.Model):
    state = models.BooleanField(default=False, verbose_name=_("Relay State"))  # True for ON, False for OFF
    
    day_of_week = models.CharField(
        max_length=9, 
        choices=[
            ('Monday', _('Monday')), 
            ('Tuesday', _('Tuesday')),
            ('Wednesday', _('Wednesday')),
            ('Thursday', _('Thursday')),
            ('Friday', _('Friday')),
            ('Saturday', _('Saturday')),
            ('Sunday', _('Sunday'))
        ],
        unique=True,
        verbose_name=_("Day of the Week")
    )
    
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))
    
    def get_current_cycle_runtime(self):
        """Gets the runtime (in seconds) for the current cycle if it matches today and the current time."""
        now = datetime.now()
        today = now.strftime('%A')
        current_time = now.time()

        if self.day_of_week == today:
            for cycle in self.cycles.all():
                start_time = cycle.start_time
                end_time = (datetime.combine(datetime.today(), start_time) + cycle.duration).time()
                
                if start_time <= current_time <= end_time:
                    runtime = (datetime.combine(datetime.today(), end_time) - now).total_seconds()
                    return runtime
        
        return 0
    
    def __str__(self):
        state_text = _("ON") if self.state else _("OFF")
        return _("{day_of_week} - {state}").format(
            day_of_week=_(self.day_of_week),
            state=state_text
        )
    
    class Meta:
        verbose_name = _("Relay State")
        verbose_name_plural = _("Relay State")


class IrrigationCycle(models.Model):
    relay_state = models.ForeignKey(RelayState, related_name='cycles', on_delete=models.CASCADE, verbose_name=_("Relay State"), db_index=True)
    start_time = models.TimeField(verbose_name=_("Start Time"))  # Time to start the pump
    duration = models.DurationField(verbose_name=_("Duration"))  # Duration to keep the pump on
    
    def __str__(self):
        return _("{day_of_week} - {start_time} for {duration}").format(
            day_of_week=_(self.relay_state.day_of_week),
            start_time=self.start_time,
            duration=self.duration
        )
    
    class Meta:
        verbose_name = _("Irrigation Cycle")
        verbose_name_plural = _("Irrigation Cycles")
        
        
class LastIrrigationCycle(models.Model):
    relay_state = models.ForeignKey(RelayState, on_delete=models.CASCADE, verbose_name=_("Relay State"))
    irrigation_cycle = models.ForeignKey(IrrigationCycle, on_delete=models.CASCADE, verbose_name=_("Irrigation Cycle"))
    timestamp = models.DateTimeField(auto_now=True, verbose_name=_("Timestamp"))

    def __str__(self):
        return str(self.irrigation_cycle)
    
    class Meta:
        verbose_name = _("Last Irrigation Cycle")
        verbose_name_plural = _("Last Irrigation Cycles")


class WaterConsumption(models.Model):
    flow_rate = models.ForeignKey(SensorData, on_delete=models.CASCADE, related_name='water_consumption', verbose_name=_("Flow Rate"))
    irrigation_cycle = models.ForeignKey(IrrigationCycle, on_delete=models.CASCADE, related_name='water_consumption', verbose_name=_("Irrigation Cycle"))
    individual_usage = models.FloatField(default=0.0, verbose_name=_("Individual Usage"))  # in liters
    total_measurement_duration_sec = models.FloatField(default=0.0, verbose_name=_("Total Measurement Duration (sec)"))
    
    def __str__(self):
        return str(self.individual_usage)
    
    class Meta:
        verbose_name = _("Water Consumption")
        verbose_name_plural = _("Water Consumption")
    

class TotalWaterUsage(models.Model):
    total_usage = models.FloatField(default=0.0, verbose_name=_("Total Usage"))  # in liters
    
    def __str__(self):
        return _("Total Water Used: {total_usage} Liters").format(
            total_usage=self.total_usage
        )
    
    class Meta:
        verbose_name = _("Total Water Usage")
        verbose_name_plural = _("Total Water Usage")