import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siteblog.settings")

app = Celery("siteblog")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "weekly_mailing": {
        "task": "blog.tasks.test_mailing",
        "schedule": crontab(
            hour="0",
            minute="0",
            day_of_week="monday",
        ),
    },
}

app.conf.beat_schedule = {
    "parsing": {
        "task": "blog.tasks.parsing",
        "schedule": crontab(
            hour="*",
            minute="0",
        ),
    },
}
