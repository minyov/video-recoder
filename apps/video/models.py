from hashlib import md5

from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.db import models

from apps.core.models import TimeStampedModel


@deconstructible
class UploadTo:
    def __init__(self, route: str):
        self.route = route

    def __call__(self, instance, filename: str) -> str:
        try:
            ext = filename.split('.')[-1]
        except ValueError:
            ext = None

        if instance.id and instance.file:
            instance_filename = instance.file.name.split("/")[-1]
            filename = instance_filename.split('.')[0]
        else:
            filename = md5((str(timezone.now()) + filename).encode()).hexdigest()

        if ext:
            filename += f'.{ext.lower()}'

        return f'{self.route}/{filename}'


class Video(TimeStampedModel):
    name = models.CharField(max_length=100)

    file = models.FileField(upload_to=UploadTo('originals'))
    preview = models.ImageField(upload_to=UploadTo('previews'), null=True, blank=True)
    mp4 = models.FileField(upload_to=UploadTo('mp4'), null=True, blank=True)
    webm = models.FileField(upload_to=UploadTo('webm'), null=True, blank=True)

    def __str__(self):
        return f'{self.id} {self.name}'
