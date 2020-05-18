import os
import tempfile
import uuid
import ffmpeg
import requests
import mimetypes
import logging

from stepik.celery import app

from django.conf import settings
from django.core.files.base import ContentFile, File

from utils import video_processor, image_processor

from .models import Video

logger = logging.getLogger(__name__)


@app.task(max_retries=3, autoretry_for=[Exception], retry_backoff=60)
def create_preview(video_id: int):
    video = Video.objects.get(id=video_id)

    with video.file.open() as file:
        resizes_image = image_processor.resize_image(
            video_processor.get_preview(file),
            width=640,
            height=360
        )

    with ContentFile(resizes_image) as content:
        video.preview.save('preview.jpg', content, save=False)
        Video.objects.filter(id=video_id).update(preview=video.preview)


@app.task(max_retries=3, autoretry_for=[Exception], retry_backoff=60)
def recode_video(video_id: int, ext: str):
    """
    Recodes video from original format to destination format (ext).
    """

    video = Video.objects.get(id=video_id)

    temp_filepath = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4()}.{ext}')

    try:
        input_stream = ffmpeg.input(video.file.path)
        audio_stream = input_stream["a"].filter_("aecho", 0.8, 0.9, 1000, 0.3)
        video_stream = input_stream["v"].filter('scale', 640, 360)
        output = ffmpeg.output(video_stream, audio_stream, temp_filepath)
        ffmpeg.run(output)

        with open(temp_filepath, 'rb') as file:
            getattr(video, ext).save(f'video.{ext}', File(file), save=False)
            Video.objects.filter(id=video_id).update(**{ext: getattr(video, ext)})
    except Exception as e:
        logger.error('Recode video error: ', exc_info=True)
        raise
    finally:
        os.remove(temp_filepath)


@app.task(max_retries=3, autoretry_for=[Exception], retry_backoff=60)
def download_video_file(video_id: int):
    """
    Downloads video file from Video object url and saves it to Video object file.
    """

    video = Video.objects.get(id=video_id)

    try:
        response = requests.get(video.url)
        mime_type = response.headers['Content-Type']
        if mime_type in settings.ALLOWED_VIDEO_MIME_TYPES:
            ext = mimetypes.guess_extension(mime_type)
            file_content = ContentFile(response.content)

            video.file.save(f'video.{ext}', file_content)
        else:
            logger.error(f'Video ({video_id}) has incorrect MIME type ({mime_type})')
    except Exception as e:
        logger.error('Download video file error: ', exc_info=True)
        raise
