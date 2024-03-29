# Generated by Django 3.1.2 on 2022-01-28 20:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_delete_contactinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100, unique=True, verbose_name='Street Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'Washington D.C.'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, verbose_name='City')),
                ('zip_code', models.PositiveIntegerField(default=27606, validators=[django.core.validators.MinValueValidator(10000, 'Zip code must contain 5 digits.'), django.core.validators.MaxValueValidator(99999, 'Zip code must contain 5 digits.')], verbose_name='Zip Code')),
                ('building_name', models.CharField(max_length=75, verbose_name='Building Name')),
                ('room', models.CharField(max_length=75, verbose_name='Room Number/Name')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='meeting_address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.meetingaddress', verbose_name='Meeting Location'),
        ),
    ]
