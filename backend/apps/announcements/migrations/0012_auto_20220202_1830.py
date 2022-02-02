# Generated by Django 3.1.2 on 2022-02-02 18:30

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0011_auto_20220201_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='body',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'description': 'The body, or main content, of an announcement which can contain various HTML elements.', 'items': {'anyOf': [{'additionalProperties': False, 'properties': {'element': {'enum': ['hr'], 'title': 'HTML Element', 'type': 'string'}}, 'required': ['element'], 'title': 'Horizontal Rule', 'type': 'object'}, {'additionalProperties': False, 'properties': {'content': {'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)', 'title': 'Paragraph Text', 'type': 'string'}, 'element': {'enum': ['p'], 'title': 'HTML Element', 'type': 'string'}}, 'required': ['element', 'content'], 'title': 'Paragraph', 'type': 'object'}, {'additionalProperties': False, 'properties': {'alt': {'title': 'Alternate Text', 'type': 'string'}, 'element': {'enum': ['img'], 'title': 'HTML Element', 'type': 'string'}, 'url': {'format': 'uri', 'title': 'Image URL', 'type': 'string'}}, 'required': ['element', 'alt', 'url'], 'title': 'Image', 'type': 'object'}, {'additionalProperties': False, 'properties': {'content': {'title': 'Header Text', 'type': 'string'}, 'element': {'enum': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], 'title': 'HTML Element', 'type': 'string'}}, 'required': ['element', 'content'], 'title': 'Header', 'type': 'object'}, {'additionalProperties': False, 'properties': {'content': {'title': 'Hyperlink Text', 'type': 'string'}, 'element': {'enum': ['a'], 'title': 'HTML Element', 'type': 'string'}, 'href': {'format': 'uri', 'title': 'Hypertext Reference', 'type': 'string'}}, 'required': ['element', 'href', 'content'], 'title': 'Anchor', 'type': 'object'}], 'title': 'Element'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Announcement Body', 'type': 'array'})], verbose_name='Announcement Body'),
        ),
    ]
