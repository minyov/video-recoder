from django.contrib import admin
from django.conf.urls import url, include

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v1/', include('apps.video.urls')),
]
