from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoViewSet, basename='videos')

urlpatterns = router.urls
