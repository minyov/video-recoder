from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^health-check/$', views.HealthCheckAPIView.as_view(), name='health-check'),
]
