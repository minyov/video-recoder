import os

from rest_framework import views, status
from rest_framework.response import Response


class HealthCheckAPIView(views.APIView):
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return Response(os.getppid(), status=status.HTTP_200_OK)
