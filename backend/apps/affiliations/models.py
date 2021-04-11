"""This module contains Django models that relate to AI at NC State's affiliations with outside organizations."""
from django.db import models


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
        upload_to='affiliates/logos/',
        # storage=  TODO
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
