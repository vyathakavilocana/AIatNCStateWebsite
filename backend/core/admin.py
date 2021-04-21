"""This module contains generic classes for customization of the Django admin site such as widgets."""
from django import forms
from django_admin_json_editor import JSONEditorWidget


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

