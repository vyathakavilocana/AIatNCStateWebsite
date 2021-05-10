"""This module contains Django models that relate to club announcements and updates."""
from django.db import models

from core.validators import JSONSchemaValidator


# TODO Docs
ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Announcement Body',
    'description': 'The body, or main content, of an announcement which can contain various HTML elements.',
    'type': 'array',
    'items': {
        'title': 'Element',
        'anyOf': [
            {
                'title': 'Horizontal Rule',
                'type': 'object',
                'properties': {
                    'element': {
                        'title': 'HTML Element',
                        'type': 'string',
                        'enum': ['hr']
                    }
                },
                'required': ['element'],
                'additionalProperties': False
            },
            {
                'title': 'Paragraph',
                'type': 'object',
                'properties': {
                    'element': {
                        'title': 'HTML Element',
                        'type': 'string',
                        'enum': ['p']
                    },
                    'content': {
                        'title': 'Paragraph Text',
                        'type': 'string'
                    }
                },
                'required': ['element', 'content'],
                'additionalProperties': False
            },
            {
                'title': 'Image',
                'type': 'object',
                'properties': {
                    'element': {
                        'title': 'HTML Element',
                        'type': 'string',
                        'enum': ['img']
                    },
                    'alt': {
                        'title': 'Alternate Text',
                        'type': 'string'
                    },
                    'url': {
                        'title': 'Image URL',
                        'type': 'string',
                        'format': 'uri'
                    }
                },
                'required': ['element', 'alt', 'url'],
                'additionalProperties': False
            },
            {
                'title': 'Header',
                'type': 'object',
                'properties': {
                    'element': {
                        'title': 'HTML Element',
                        'type': 'string',
                        'enum': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                    },
                    'content': {
                        'title': 'Header Text',
                        'type': 'string'
                    }
                },
                'required': ['element', 'content'],
                'additionalProperties': False
            }
        ]
    }
}


class Announcement(models.Model):
    """A Django database model which represents a club announcement or update.

    In the PostgreSQL database, an announcement has a title, body of content, and the date and time that it was created.
    The schema used to validate an announcement's body content, as represented in JSON, is defined above by the global
    ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA.

    Attributes:  # noqa
        title: A CharField containing the announcement's title.

        body: A JSONField containing a JSON representation of the announcement's body or content.

        created: A DateTimeField that contains the date and time that the announcement was created.
    """

    title = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=True,
        verbose_name='Announcement Title'
    )
    body = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA)],
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Announcement Body'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
        editable=False,
        unique=False,
        verbose_name='Announcement Creation Time/Date'
    )

    def __str__(self):
        """Defines the string representation of the Announcement class.

        The string representation of an Announcement class instance only contains the title of the announcement.

        Returns:
            A string containing the announcement's title.
        """
        return self.title

    class Meta:
        """TODO Docs
        """
        ordering = ['-created']
