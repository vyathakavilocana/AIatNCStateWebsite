"""This module contains core Admin site functionality."""
from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline
from django_admin_json_editor import JSONEditorWidget

from core.models import ContactInfo


class ContactInfoTabularInline(GenericTabularInline):
    """Defines an inline Django admin element to add/edit contact information on the event admin page.

    TODO Update Docs

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


class ReadOnlyContactInfoTabularInline(ContactInfoTabularInline):
    """TODO Docs
    """
    def has_change_permission(self, request, obj=None):
        """TODO Docs
        """
        return False

    def has_add_permission(self, request, obj=None):
        """TODO Docs
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """TODO Docs
        """
        return False


class JSONFieldEditorWidget(JSONEditorWidget):
    """A generic Django widget for editing JSON field data.
    """
    def __init__(self, schema):
        """Override the JSONEditorWidget initialization method to only allow one parameter and pass it default values.

        All instances of this widget in forms site-wide will be initialized without being collapsed, overriding the
        super class' default behavior.

        Args:
            schema: A dictionary containing a JSON schema for constructing the widget and performing data validation.
        """
        super().__init__(schema, collapsed=False)

    @property
    def media(self):
        """Override the JSONEditorWidget class' media property to fix errors and add custom styling.

        By default, there is an error with the serving of the Bootstrap stylesheet included with the
        `django-admin-json-editor` package, so the path to that file has been overridden with a link to a CDN that
        serves a minified Bootstrap 4 stylesheet. Additionally, a custom stylesheet is included to hide the widget's
        built-in collapse button.
        """
        css = {
            'all': [
                'django_admin_json_editor/fontawesome/css/font-awesome.min.css',
                'django_admin_json_editor/style.css',
                'admin/json-editor-widget.css',  # Custom stylesheet
            ]
        }
        js = [
            'django_admin_json_editor/jsoneditor/jsoneditor.min.js',
        ]

        if self._editor_options['theme'] == 'bootstrap4':
            css['all'].append('https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css')
            js.append('django_admin_json_editor/jquery/jquery-3.5.1.slim.min.js')
            js.append('django_admin_json_editor/bootstrap/js/bootstrap.bundle.min.js')

        if self._sceditor:
            css['all'].append('django_admin_json_editor/sceditor/themes/default.min.css')
            js.append('django_admin_json_editor/sceditor/jquery.sceditor.bbcode.min.js')
        return forms.Media(css=css, js=js)

