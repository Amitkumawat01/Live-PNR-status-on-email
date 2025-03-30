from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PNRStatusTracker.settings')

app = Celery('MainApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-pnr-status-every-10-minutes': {
        'task': 'MainApp.tasks.send_pnr_status_on_update',
        'schedule': crontab(minute='*/10'),
    },
}