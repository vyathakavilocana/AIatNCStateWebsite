from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import JSONSchemaValidator


# TODO Docs
PROJECT_AUTHORS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Project Authors',
    'description': 'A list of authors\' names (as strings) of a group project.',
    'type': 'array',
    'minItems': 1,
    'items': {
        'type': 'string',
        'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)'
    }
}

# TODO Docs
#  Define the base file path, which will be appended to the MEDIA_ROOT directory, where affiliate logos should be saved.
BASE_IMAGE_PATH = 'projects/'


def image_path(instance, filename):
    """TODO Docs

    This callable is used by the Affiliate class' logo field to evaluate the path at which to save a logo.

    Args:
        instance: An instance of the Affiliate class, from which the name of the affiliate is used to build the final
            path for the logo.
        filename: The name of the file, from which the file extension is used to build the final path for the logo.

    Returns:
        The path where the uploaded affiliate logo should be saved.
    """
    # Build the name of the logo file, replacing the following invalid characters: `/` and `\0`.
    name = instance.name.lower() \
                        .replace(' ', '_') \
                        .replace('/', '') \
                        .replace('\0', '')
    extension = filename[filename.rindex('.'):]  # Includes the `.`

    return f'{BASE_IMAGE_PATH}{name}/main_image{extension}'


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
        max_length=250,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=True,
        verbose_name='Project Title'
    )
    authors = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=PROJECT_AUTHORS_FIELD_JSON_SCHEMA)],
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Project Authors'
    )
    description = models.TextField(
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Project Description'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        editable=True,
        unique=True,
        verbose_name='Project Image',
        upload_to=image_path
    )
    url = models.URLField(
        null=True,
        blank=True,
        editable=True,
        unique=True,
        verbose_name='External Project URL',
        max_length=200
    )
    status = models.CharField(
        max_length=2,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNED,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Project Status or Phase'
    )
    modified = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=True,
        editable=False,
        unique=False,
        verbose_name='Date and Time of Last Edit'
    )

    def __str__(self):
        """TODO Docs
        """
        # TODO Implementation
        pass
