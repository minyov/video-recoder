from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Video
from .tasks import create_preview


@receiver(post_save, sender=Video)
def video_post_save(instance: Video, **kwargs):
    if instance.id and not instance.preview:
        create_preview.delay(video_id=instance.id)
