"""TODO Docs"""
from celery import shared_task

from apps.announcements.models import Announcement


@shared_task
def project_created(name, authors, description, url):  # TODO
    """TODO Docs
    """
    announcement = Announcement(
        title='New Project!',
        body=[
            {
                'element': 'h3',
                'content': name
            },
            {
                'element': 'h6',
                'content': ', '.join(authors)
            },
            {
                'element': 'p',
                'content': description
            },
            {
                'element': 'hr'
            },
            {
                'element': 'a',
                'href': url,
                'content': 'Read More'
            }
        ]
    )
    announcement.save()
