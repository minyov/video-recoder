from rest_framework import serializers

from . import models


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = '__all__'
        read_only_fields = (
            'preview',
            'mp4',
            'webm'
        )
