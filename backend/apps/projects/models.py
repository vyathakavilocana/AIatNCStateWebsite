from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.validators import JSONSchemaValidator


# TODO Docs
PROJECT_AUTHORS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Project Authors',
    'description': 'A list of authors\' names (as strings) of a project event.',
    'type': 'array',
    'properties': {
        'items': {
            'type': 'string'
        }
    }
}


class Project(models.Model):
    """
    TODO Docs
    """

    class ProjectStatus(models.TextChoices):
        """
        TODO Docs
        """
        COMPLETE = 'CO', _('Complete')
        IN_PROGRESS = 'IP', _('In Progress')
        PLANNED = 'PL', _('Planned')
        OTHER = 'OT', _('Other')
        # TODO

    name = models.CharField(
        max_length=5,
        # TODO
    )
    authors = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=PROJECT_AUTHORS_FIELD_JSON_SCHEMA)],
        # TODO
    )
    description = models.TextField(
        # TODO
    )
    image = models.ImageField(
        # TODO
    )
    url = models.URLField(
        # TODO
    )
    status = models.CharField(
        max_length=2,
        choices=ProjectStatus.choices,
        # TODO
    )
    modified = models.DateTimeField(
        auto_now=True,
        # TODO
    )
