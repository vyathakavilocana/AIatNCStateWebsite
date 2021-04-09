from django.db import models

from apps.validators import JSONSchemaValidator


# TODO Docs
ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Announcement Body',
    'description': 'The body, or main content, of an announcement which can contain various HTML elements.',
    'type': 'array',
    'items': {
        'anyOf': [
            {'$ref': '#/$defs/horizontalRule'},
            {'$ref': '#/$defs/paragraph'},
            {'$ref': '#/$defs/image'},
            {'$ref': '#/$defs/header'},
        ]
    },
    '$defs': {
        'horizontalRule': {
            'type': 'object',
            'properties': {
                'element': {'type': 'string', 'enum': ['hr']}
            },
            'required': ['element'],
            'additionalProperties': False
        },
        'paragraph': {
            'type': 'object',
            'properties': {
                'element': {'type': 'string', 'enum': ['p']},
                'content': {'type': 'string'}
            },
            'required': ['element', 'content'],
            'additionalProperties': False
        },
        'image': {
            'type': 'object',
            'properties': {
                'element': {'type': 'string', 'enum': ['img']},
                'alt': {'type': 'string'},
                'url': {'type': 'string'}
            },
            'required': ['element', 'alt', 'url'],
            'additionalProperties': False
        },
        'header': {
            'type': 'object',
            'properties': {
                'element': {'type': 'string', 'enum': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']},
                'content': {'type': 'string'}
            },
            'required': ['element', 'content'],
            'additionalProperties': False
        }
    }
}


class Announcement(models.Model):
    """
    TODO Docs
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
