from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    # Django loads signals only if the app’s ready() method imports them.
    def ready(self):
        import messaging.signals
