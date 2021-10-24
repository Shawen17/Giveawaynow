from django.apps import AppConfig


class GiversConfig(AppConfig):
    name = 'givers'

    def ready(self):
        from giftUpdater import update
        update.start()
