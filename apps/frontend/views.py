from django.shortcuts import render
from django.views import View
from django.conf import settings

from apps.video.models import Video


class MainView(View):
    def get(self, request):
        videos = Video.objects.all()

        allowed_mime_types = settings.ALLOWED_VIDEO_MIME_TYPES

        return render(request, 'frontend/index.html', locals())
