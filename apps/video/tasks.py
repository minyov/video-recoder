import os
import tempfile
import uuid
import ffmpeg

from stepik.celery import app

from django.core.files.base import ContentFile, File

from utils import video_processor, image_processor

from .models import Video


@app.task
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


@app.task
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
        print(e)
    finally:
        os.remove(temp_filepath)
