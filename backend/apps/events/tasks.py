from celery import shared_task

from apps.announcements.models import Announcement
from apps.events.models import Event


@shared_task
def event_created_announcement(pk):
    """TODO Docs
    """
    pass


@shared_task
def event_updated_announcement(pk):
    """TODO Docs
    """
    pass
