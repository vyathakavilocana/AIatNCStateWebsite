"""This module contains custom Django forms for creating announcement app model instances."""
from django import forms

from core.admin import JSONFieldEditorWidget
from apps.announcements.models import Announcement, ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA


class AnnouncementModelAdminForm(forms.ModelForm):
    """A simple, custom form for creating Announcement model instances.
    """
    class Meta:
        """Defines metadata options for the containing `AnnouncementModelAdminForm` class.

        Among these options are the model the form allows the creation and editing of (the `Announcement` model), an
        option to include all of the model's fields in the form, and an override for the default `JSONField` widget to
        instead utilize a custom `JSONFieldEditorWidget` for the body field.
        """
        model = Announcement
        fields = '__all__'
        widgets = {
            'body': JSONFieldEditorWidget(ANNOUNCEMENT_BODY_FIELD_JSON_SCHEMA),
        }
