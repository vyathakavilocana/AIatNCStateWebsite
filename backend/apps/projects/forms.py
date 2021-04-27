"""This module contains custom Django forms for creating projects app model instances."""
from django import forms

from core.admin import JSONFieldEditorWidget
from .models import Project, PROJECT_AUTHORS_FIELD_JSON_SCHEMA


class ProjectModelAdminForm(forms.ModelForm):
    """A simple, custom form for creating Project model instances.
    """
    class Meta:
        """Defines metadata options for the containing `ProjectModelAdminForm` class.

        Among these options are the model the form allows the creation and editing of (the `Project` model), an option
        to include all of the model's fields in the form, and an override for the default `JSONField` widget to instead
        utilize a custom `JSONFieldEditorWidget` for the authors field.
        """
        model = Project
        fields = '__all__'
        widgets = {
            'topics': JSONFieldEditorWidget(PROJECT_AUTHORS_FIELD_JSON_SCHEMA),
        }

