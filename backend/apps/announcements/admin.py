"""This module contains announcement application configuration for the Django admin site.

This configuration allows announcements application model instances to be viewed, created, edited, and deleted on the
Django administrator site.
"""
from django.contrib import admin

from .models import Announcement


# Register the Announcement model with the Django admin site.
admin.site.register(Announcement)
