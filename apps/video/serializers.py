from django.conf import settings

from rest_framework import serializers

from . import models


class VideoSerializer(serializers.ModelSerializer):
    def validate_file(self, file):
        if file.content_type not in settings.ALLOWED_VIDEO_MIME_TYPES:
            raise serializers.ValidationError('File MIME type is not allowed')

        return file

    class Meta:
        model = models.Video
        fields = '__all__'
        read_only_fields = (
            'preview',
            'mp4',
            'webm'
        )
