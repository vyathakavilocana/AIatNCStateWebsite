"""This module contains a simple configuration for the contact Django application."""
from django.apps import AppConfig


class ContactConfig(AppConfig):
    """A simple Django application configuration class which only contains the name for the contact Django app.

    Attributes:  # noqa
        name: A string containing the name of the contact app. The same name is included in the config.settings module's
        list of installed apps, ``INSTALLED_APPS``, so that this application is properly registered by Django.
    """
    name = 'contact'
