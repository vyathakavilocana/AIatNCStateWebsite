"""This module contains custom Django forms for creating events app model instances."""
from django import forms

from core.admin import JSONFieldEditorWidget
from .models import Event, EVENT_TOPICS_FIELD_JSON_SCHEMA


class EventModelAdminForm(forms.ModelForm):
    """A simple, custom form for creating Event model instances.
    """
    class Meta:
        """Defines metadata options for the containing `EventModelAdminForm` class.

        Among these options are the model the form allows the creation and editing of (the `Event` model), an option to
        include all of the model's fields in the form, and an override for the default `JSONField` widget to instead
        utilize a custom `JSONFieldEditorWidget` for the topics field.
        """
        model = Event
        fields = '__all__'
        widgets = {
            'topics': JSONFieldEditorWidget(EVENT_TOPICS_FIELD_JSON_SCHEMA),
        }
