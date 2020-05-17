from hashlib import md5

from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.db import models

from apps.core.models import TimeStampedModel


@deconstructible
class UploadTo:
    """
    Class to control paths of storing files.
    """

    def __init__(self, route: str):
        self.route = route

    def __call__(self, instance, filename: str) -> str:
        try:
            ext = filename.split('.')[-1]
        except ValueError:
            ext = None

        if instance.id and instance.file:
            file_name = instance.file_name
        else:
            file_name = md5((str(timezone.now()) + filename).encode()).hexdigest()

        if ext:
            file_name += f'.{ext.lower()}'

        return f'{self.route}/{file_name}'


class Video(TimeStampedModel):
    url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to=UploadTo('originals'), null=True, blank=True)
    preview = models.ImageField(upload_to=UploadTo('previews'), null=True, blank=True)
    mp4 = models.FileField(upload_to=UploadTo('mp4'), null=True, blank=True)
    webm = models.FileField(upload_to=UploadTo('webm'), null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    @property
    def full_file_name(self):
        return self.file.name.split('/')[-1]

    @property
    def file_name(self):
        return self.full_file_name.split('.')[0]

    @property
    def file_ext(self):
        return self.full_file_name.split('.')[-1]

    @property
    def processed(self):
        return all((self.file, self.preview, self.mp4, self.webm))
