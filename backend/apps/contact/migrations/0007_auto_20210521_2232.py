# Generated by Django 3.1.2 on 2021-05-21 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_auto_20210520_2313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admincomment',
            options={'verbose_name': 'Administrator Comment'},
        ),
        migrations.AlterModelOptions(
            name='contactformbase',
            options={'ordering': ['-submitted'], 'verbose_name': 'Submitted Contact Form'},
        ),
    ]