"""This module contains announcement application configuration for the Django admin site.

This configuration allows announcements application model instances to be viewed, created, edited, and deleted on the
Django administrator site.
"""
from django.contrib import admin

from .models import Announcement
from .forms import AnnouncementModelAdminForm


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Defines a typical Django model admin page for the Project model.

    Attributes:  # noqa
        form: The custom ModelForm for use in creating/editing Announcement objects.
    """
    form = AnnouncementModelAdminForm
