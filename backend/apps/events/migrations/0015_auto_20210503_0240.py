# Generated by Django 3.1.2 on 2021-05-03 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20210503_0138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start']},
        ),
    ]