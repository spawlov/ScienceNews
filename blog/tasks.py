import os
import smtplib
import subprocess
import sys
from datetime import timedelta

from celery import shared_task

from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Subscriber


@shared_task
def weekly_mailing():
    site = settings.ALLOWED_HOSTS[0]
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(
        created_at__gte=last_week,
        published=True,
    ).order_by("created_at")
    subscribers = list(
        Subscriber.objects.all().values_list("email", flat=True),
    )
    for subscriber in subscribers:
        with mail.get_connection() as connection:
            html_content = render_to_string(
                template_name="blog/email_templates/week_email.html",
                context={
                    "site": site,
                    "posts": posts,
                    "email": subscriber,
                },
            )
            message = mail.EmailMultiAlternatives(
                subject="Test message from Science News",
                from_email=settings.EMAIL,
                to=[subscriber],
                connection=connection,
            )
            message.attach_alternative(html_content, "text/html")
            try:
                message.send()
            except (
                smtplib.SMTPConnectError,
                smtplib.SMTPAuthenticationError,
                smtplib.SMTPDataError,
                smtplib.SMTPHeloError,
                smtplib.SMTPNotSupportedError,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPException,
            ) as error:
                return str(error)
            return "Email sent successfully"


@shared_task()
def parsing():
    python_path = sys.executable
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manage_path = os.path.join(project_path, "manage.py")
    subprocess.run(
        [
            python_path,
            manage_path,
            "parsing_naked_science",
        ],
    )
    return "Parsing finished successfully"
