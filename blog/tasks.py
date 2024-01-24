from celery import shared_task

from django.core.management import execute_from_command_line


@shared_task
def parsing():
    execute_from_command_line(["manage.py", "parsing_naked_science"])
