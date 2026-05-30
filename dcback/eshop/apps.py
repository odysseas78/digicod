import os

from django.apps import AppConfig


class EshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eshop'
    def ready(self):
        import eshop.signals
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
