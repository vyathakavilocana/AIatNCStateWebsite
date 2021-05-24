"""This module contains events application configuration for the Django admin site.

This configuration allows events application model instances to be viewed, created, edited, and deleted on the Django
administrator site.
"""
from django.contrib import admin

from core.admin import ContactInfoTabularInline
from apps.events.models import Event
from apps.events.forms import EventModelAdminForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Defines a typical Django model admin page with a single inline Django model admin for related ContactInfo models.

    Attributes:  # noqa
        inlines: A list of inline Django model admin classes to include on the Event admin page.

        form: The custom ModelForm for use in creating/editing Event objects.
    """
    inlines = [
        ContactInfoTabularInline,
    ]
    form = EventModelAdminForm
