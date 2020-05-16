from django.apps import AppConfig


class VideoConfig(AppConfig):
    name = 'apps.video'

    def ready(self):
        from . import signals
