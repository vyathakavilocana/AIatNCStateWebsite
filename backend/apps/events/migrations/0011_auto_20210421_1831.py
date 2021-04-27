# Generated by Django 3.1.2 on 2021-04-21 18:31

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20210421_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='topics',
            field=models.JSONField(blank=True, default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'items': {'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)', 'title': 'Topic', 'type': 'string'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Event Topics', 'type': 'array'})], verbose_name='Event Topics'),
        ),
    ]