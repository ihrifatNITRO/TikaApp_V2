# TikaApp/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TikaApp.settings')
app = Celery('TikaApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()