from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "router.settings")

app = Celery("router")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# RedBeat configuration
app.conf.beat_schedule = {
    "update-all-data-every-midnight": {
        "task": "financial_data_engine.tasks.update_all_data",
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
}

app.conf.redbeat_redis_url = "redis://redis:6379/1"

app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_color=False,
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",
    worker_log_level="INFO",
)
