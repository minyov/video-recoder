from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Video
from .tasks import create_preview, recode_video, download_video_file
from .enums import VideoMimeTypeEnum


@receiver(post_save, sender=Video)
def video_post_save(instance: Video, created: bool, **kwargs):
    if created:
        if instance.file:
            start_processing_video(instance.id)
        elif instance.url:
            download_video_file.delay(video_id=instance.id)


@receiver(post_save, sender=Video)
def video_file_downloaded_by_url_post_save(instance: Video, created: bool, **kwargs):
    if all((not created, instance.file, instance.url)):
        start_processing_video(instance.id)


def start_processing_video(video_id: int):
    create_preview.delay(video_id=video_id)
    recode_video.delay(video_id=video_id, ext=VideoMimeTypeEnum.WEBM.value)
    recode_video.delay(video_id=video_id, ext=VideoMimeTypeEnum.MP4.value)
