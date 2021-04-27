"""This module contains a simple configuration for the projects Django application."""
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """A simple Django application configuration class which only contains the name for the events Django app.

    Attributes:  # noqa
        name: A string containing the name of the projects app. The same name is included in the config.settings
        module's list of installed apps, ``INSTALLED_APPS``, so that this application is properly registered by Django.
    """
    name = 'projects'
