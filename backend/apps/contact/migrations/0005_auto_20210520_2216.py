# Generated by Django 3.1.2 on 2021-05-20 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20210520_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnercontactform',
            name='max_org_size',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='Estimated Maximum Size of Organization'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='min_org_size',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='Estimated Minimum Size of Organization'),
        ),
    ]
