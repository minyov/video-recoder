from stepik.celery import app

from django.core.files.base import ContentFile

from utils import video_processor, image_processor

from .models import Video


@app.task
def create_preview(video_id: int):
    video = Video.objects.get(id=video_id)

    with video.file.open() as file:
        compressed_image = image_processor.compress_image(
            video_processor.get_preview(file),
            width=640,
            height=360
        )

    with ContentFile(compressed_image) as content:
        video.preview.save('preview.jpg', content)
