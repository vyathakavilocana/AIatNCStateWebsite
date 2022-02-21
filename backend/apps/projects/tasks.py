"""This module contains asynchronous Celery tasks for the Project application."""
from celery import shared_task

from apps.announcements.models import Announcement


@shared_task
def project_created(name, authors, description, url):
    """Creates a new Announcement indicating that a new Project was created.

    Args:
        name: the name of the project
        authors: a list of the project's authors
        description: a description of the project
        url: the relative url for the project's individual detail page
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
