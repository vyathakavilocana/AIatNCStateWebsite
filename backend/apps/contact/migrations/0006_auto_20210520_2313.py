# Generated by Django 3.1.2 on 2021-05-20 23:13

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_auto_20210520_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='availability',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'items': {'additionalProperties': False, 'properties': {'date': {'format': 'date', 'title': 'Date', 'type': 'string'}, 'time': {'format': 'time', 'title': 'Time', 'type': 'string'}}, 'required': ['date', 'time'], 'title': 'Date/Time of Availability'}, 'maxItems': 3, 'minItems': 1, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Availability', 'type': 'array'})], verbose_name='Availability'),
        ),
    ]
