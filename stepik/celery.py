import os

from datetime import timedelta

from celery import Celery

EXPIRE_TIME = 60 * 60 * 24

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stepik.settings')

app = Celery('stepik')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.result_expires = timedelta(seconds=EXPIRE_TIME)
app.autodiscover_tasks()

