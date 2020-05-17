from django.shortcuts import render, reverse, redirect
from django.views import View

from apps.video.models import Video


class MainView(View):
    def get(self, request):
        videos = Video.objects.all()

        return render(request, 'frontend/index.html', locals())
