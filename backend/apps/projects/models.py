"""This module contains Django models that relate to group projects."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import JSONSchemaValidator


# A JSON schema used in validating the authors field of the Projects model. This field is only valid if it contains a
# JSON array whose elements are strings that are not empty and that do not only contain whitespace. Since projects must
# have at least one author, the array cannot be empty.
PROJECT_AUTHORS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Project Authors',
    'type': 'array',
    'minItems': 1,
    'items': {
        'type': 'string',
        'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)'
    }
}

# Define the base file path, which will be appended to the MEDIA_ROOT directory, where project images should be saved.
BASE_IMAGE_PATH = 'projects/images/'


def image_path(instance, filename):
    """This callable is used by the Project class' `image` field to evaluate the path at which to save a project image.

    Args:
        instance: An instance of the Project class, from which the title of the project is used to build the final
        path for the logo.
        filename: The name of the file, from which the file extension is used to build the final path for the image.

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
    """A Django database model which represents a group project.

    In the PostgreSQL database, a project has a name, a list of authors, a description, an image, a URL for an external
    website where the project (or its code) is hosted, a status (complete, in progress, etc.), and the date and time the
    project was last edited.

    Attributes:  # noqa
        name: A CharField containing the name of the project.

        authors: A JSONField containing a JSON representation of a list of project authors as strings.

        description: A TextField containing a long-form description of the project.

        image: An ImageField representing the project's image in the database.

        url: An optional URLField containing a link to an external website where the project is hosted (e.g., github).

        status: A CharField containing the status of the project. The available statuses are defined in the
        ProjectStatus class.

        modified: A DateTimeField containing the date and time when the project was last edited.
    """

    class ProjectStatus(models.TextChoices):
        """Defines the supported statuses of projects for the Project model's ``status`` field.

        Attributes:  # noqa
            COMPLETE: A 2 character identifier and lazily-evaluated label representing the choice of the project being
            finished/finalized.

            IN_PROGRESS: A 2 character identifier and lazily-evaluated label representing the choice of the project
            being in progress and still being actively worked on.

            PLANNED: A 2 character identifier and lazily-evaluated label representing the choice of the project being
            planned for the future.

            OTHER: A 2 character identifier and lazily-evaluated label representing the catch-all choice for all other
            statuses of projects.
        """
        COMPLETE = 'CO', _('Complete')
        IN_PROGRESS = 'IP', _('In Progress')
        PLANNED = 'PL', _('Planned')
        OTHER = 'OT', _('Other')

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
        """Defines the string representation of the Project model.

        The string representation of a Project object only contains the project's name.

        Returns:
            A string containing the project's name.
        """
        return self.name
