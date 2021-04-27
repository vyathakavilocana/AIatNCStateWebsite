# Generated by Django 3.1.2 on 2021-04-27 14:21

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210420_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='authors',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'items': {'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)', 'type': 'string'}, 'minItems': 1, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Project Authors', 'type': 'array'})], verbose_name='Project Authors'),
        ),
    ]
