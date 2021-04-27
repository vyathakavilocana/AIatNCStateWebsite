"""This module contains projects application configuration for the Django admin site.

This configuration allows projects application model instances to be viewed, created, edited, and deleted on the Django
administrator site.
"""
from django.contrib import admin

from .models import Project
from .forms import ProjectModelAdminForm


@admin.register(Project)
class EventAdmin(admin.ModelAdmin):
    """Defines a typical Django model admin page for the Project model.

    Attributes:  # noqa
        form: The custom ModelForm for use in creating/editing Event objects.
    """
    form = ProjectModelAdminForm
