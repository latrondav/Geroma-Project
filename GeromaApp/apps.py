from django.apps import AppConfig


class GeromaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GeromaApp'

    def ready(self):
        import GeromaApp.signals