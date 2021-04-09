from django.db import models


class Affiliate(models.Model):
    """
    TODO Docs
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
