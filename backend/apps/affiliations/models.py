"""This module contains Django models that relate to AI at NC State's affiliations with outside organizations."""
from django.dispatch import receiver
from django.db import models


# Define the base file path, which will be appended to the MEDIA_ROOT directory, where affiliate logos should be saved.
BASE_LOGO_PATH = 'affiliates/logos/'


def logo_path(instance, filename):
    """This callable is used by the Affiliate class' logo field to evaluate the path at which to save a logo.

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

    return f'{BASE_LOGO_PATH}{name}{extension}'


class Affiliate(models.Model):
    """A Django database model which represents an affiliate organization.

    In the PostgreSQL database, an affiliate has a name, logo, and website URL.

    Attributes:  # noqa
        name: A CharField representing the affiliate's name in the database.

        logo: An ImageField representing the affiliate's logo in the database.

        website: A URLField representing the affiliate's website URL in the database.
    """

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=True,
        verbose_name='Affiliate Name'
    )
    logo = models.ImageField(
        null=True,
        blank=True,
        editable=True,
        unique=True,
        verbose_name='Affiliate Logo',
        upload_to=logo_path
    )
    website = models.URLField(
        null=False,
        blank=False,
        editable=True,
        unique=True,
        verbose_name='Affiliate Website URL',
        max_length=150
    )

    def __str__(self):
        """Defines the string representation of the Affiliate class.

        The string representation of an Affiliate class instance only contains the name of the company or organization
        which it represents.

        Returns:
            A string containing the affiliate's name.
        """
        return self.name


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Affiliate)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes the logo file of an Affiliate model object when the object is in the process of being deleted.

    Reference: https://stackoverflow.com/a/16041527
    """
    instance.logo.delete(save=False)
