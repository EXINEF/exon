from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    # Import signals for doing automatic actions
    def ready(self):
    	import app.signals
