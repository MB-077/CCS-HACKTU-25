from django.apps import AppConfig


class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sensors'
    
    def ready(self):
        import Sensors.signals
        import utils.mongo_connection
