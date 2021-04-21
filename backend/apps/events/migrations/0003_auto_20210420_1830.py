# Generated by Django 3.1.2 on 2021-04-20 18:30

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20210411_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='topics',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'description': 'A list of topics (as strings) for an event.', 'items': {'pattern': '(^(?!\\s*$))|(^.*\\S.*$)', 'type': 'string'}, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Event Topics', 'type': 'array'})], verbose_name='Event Topics'),
        ),
    ]