# Generated by Django 3.1.2 on 2021-05-24 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210507_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'ordering': ['preferred']},
        ),
    ]
