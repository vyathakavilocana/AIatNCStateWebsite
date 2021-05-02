"""This module contains events application configuration for the Django admin site.

This configuration allows events application model instances to be viewed, created, edited, and deleted on the Django
administrator site.
"""
from django.contrib import admin

from .models import ContactInfo, Event
from .forms import EventModelAdminForm


class ContactInfoStackedInline(admin.StackedInline):
    """Defines an inline Django admin element to add/edit contact information on the event admin page.

    Rather than have separate administrator pages for the ContactInfo and Event models, we have the ability to edit the
    "nested" ContactInfo model instances that are related to an Event model instance directly on the Event model admin
    page. This avoids confusion that could arise in creating a ContactInfo instance separately, then having to manually
    set which event in the database the ContactInfo is related to.

    Attributes:  # noqa
        model: The model class that this inline model admin allows the creation/editing of (ContactInfo).

        extra: The number of "new" ContactInfo's are displayed on the admin page by default.

        verbose_name: A long-form, singular name for the inline to be displayed on the admin site.

        verbose_name_plural: A long-form, plural name for the inline to be displayed on the admin site.
    """
    model = ContactInfo
    extra = 1
    verbose_name = 'Point of Contact'
    verbose_name_plural = 'Points of Contact'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Defines a typical Django model admin page with a single inline Django model admin for related ContactInfo models.

    Attributes:  # noqa
        inlines: A list of inline Django model admin classes to include on the Event admin page.

        form: The custom ModelForm for use in creating/editing Event objects.
    """
    inlines = [
        ContactInfoStackedInline,
    ]
    form = EventModelAdminForm
