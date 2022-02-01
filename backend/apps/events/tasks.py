"""TODO Docs"""
from celery import shared_task
from django.template.loader import render_to_string

from apps.announcements.models import Announcement


@shared_task
def event_created(event_type, start):
    """TODO Docs
    """
    announcement = Announcement(
        title='New Event!',
        body=[{
            'element': 'p',
            'content': render_to_string(
                'event/created_body.txt',
                context={
                    'type': event_type,
                    'start': start
                }
            )
        }]
    )
    announcement.save()


@shared_task
def event_rescheduled(event_type, start):
    """TODO Docs
    """
    announcement = Announcement(
        title='Event Rescheduled',
        body=[{
            'element': 'p',
            'content': render_to_string(
                'event/rescheduled_body.txt',
                context={
                    'type': event_type,
                    'start': start
                }
            )
        }]
    )
    announcement.save()
