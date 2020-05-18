from django.apps import AppConfig
from django.conf import settings


class VideoConfig(AppConfig):
    name = 'apps.video'

    def ready(self):
        if not settings.IS_TEST_ENVIRONMENT:
            from . import signals
