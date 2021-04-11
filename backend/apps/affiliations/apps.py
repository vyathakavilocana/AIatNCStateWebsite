"""This module contains a simple configuration for the affiliations Django application."""
from django.apps import AppConfig


class AffiliationsConfig(AppConfig):
    """A simple Django application configuration class which only contains the name for the affiliations Django app.

    Attributes:  # noqa
        name: A string containing the name of the affiliations app. The same name is included in the config.settings
        module's list of installed apps, ``INSTALLED_APPS``, so that this application is properly registered by Django.
    """
    name = 'affiliations'
