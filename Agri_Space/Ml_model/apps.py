from django.apps import AppConfig


class MlModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ml_model'
    
    def ready(self):
        import Ml_model.signals
