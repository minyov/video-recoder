from rest_framework import viewsets, mixins, parsers

from . import models, serializers


class VideoViewSet(mixins.CreateModelMixin,
                   viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.VideoSerializer
    queryset = models.Video.objects.all()
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
