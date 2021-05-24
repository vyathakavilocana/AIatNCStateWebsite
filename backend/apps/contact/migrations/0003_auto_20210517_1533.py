# Generated by Django 3.1.2 on 2021-05-17 15:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20210517_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformbase',
            name='submitted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date/Time Submitted'),
            preserve_default=False,
        ),
    ]