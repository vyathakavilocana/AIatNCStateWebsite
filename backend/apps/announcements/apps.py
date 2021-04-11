"""This module contains a simple configuration for the announcements Django application."""
from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    """A simple Django application configuration class which only contains the name for the announcements Django app.

    Attributes:  # noqa
        name: A string containing the name of the announcements app. The same name is included in the config.settings
        module's list of installed apps, ``INSTALLED_APPS``, so that this application is properly registered by Django.
    """
    name = 'announcements'
