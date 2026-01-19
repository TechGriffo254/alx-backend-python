from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

# Create Celery app
app = Celery('messaging_app')

# Load config from Django settings with 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Configure Celery broker and backend from environment variables
app.conf.update(
    broker_url=config('CELERY_BROKER_URL', default='amqp://guest:guest@localhost:5672//'),
    result_backend=config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
