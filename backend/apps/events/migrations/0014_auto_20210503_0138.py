# Generated by Django 3.1.2 on 2021-05-03 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20210421_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', related_query_name='contacts', to='events.event', verbose_name='Associated Event'),
        ),
    ]
