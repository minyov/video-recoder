from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Video
from .tasks import create_preview, recode_video
from .enums import VideoMimeTypeEnum


@receiver(post_save, sender=Video)
def video_post_save(instance: Video, created: bool, **kwargs):
    if created:
        create_preview.delay(video_id=instance.id)
        recode_video.delay(video_id=instance.id, ext=VideoMimeTypeEnum.WEBM.value)
        recode_video.delay(video_id=instance.id, ext=VideoMimeTypeEnum.MP4.value)

