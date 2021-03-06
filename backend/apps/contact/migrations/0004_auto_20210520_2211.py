# Generated by Django 3.1.2 on 2021-05-20 22:11

import core.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20210517_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admincomment',
            name='first_name',
            field=models.CharField(default='', max_length=80, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='admincomment',
            name='last_name',
            field=models.CharField(default='', max_length=80, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='affiliation',
            field=models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Affiliate Organization'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='first_name',
            field=models.CharField(default='', max_length=80, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='ignored',
            field=models.BooleanField(default=False, verbose_name='Ignored?'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='last_name',
            field=models.CharField(default='', max_length=80, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='reviewed',
            field=models.BooleanField(default=False, verbose_name='Form Reviewed?'),
        ),
        migrations.AlterField(
            model_name='contactformbase',
            name='thoughts',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Additional Thoughts/Questions/Concerns'),
        ),
        migrations.AlterField(
            model_name='eventorganizercontactform',
            name='advertising',
            field=models.TextField(default='', verbose_name='Event Advertising Campaign Information'),
        ),
        migrations.AlterField(
            model_name='eventorganizercontactform',
            name='event_type',
            field=models.CharField(default='', max_length=120, verbose_name='Type of Event to Organize'),
        ),
        migrations.AlterField(
            model_name='eventorganizercontactform',
            name='financial_assistance',
            field=models.BooleanField(default=False, verbose_name='Financial Assistance from Club Required?'),
        ),
        migrations.AlterField(
            model_name='eventorganizercontactform',
            name='max_attendees',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Estimated/Desired Maximum Number of Attendees'),
        ),
        migrations.AlterField(
            model_name='eventorganizercontactform',
            name='min_attendees',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Estimated/Desired Minimum Number of Attendees'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='addl_tech',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Additional Tech Setup Required'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='addl_visual_aids',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Additional Visual Aids Required'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='availability',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'items': {'title': 'Date/Time of Availability'}, 'maxItems': 3, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Availability', 'type': 'array'})], verbose_name='Availability'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='consent_audio_rec',
            field=models.BooleanField(default=False, verbose_name='Consent to Record Audio'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='consent_materials',
            field=models.BooleanField(default=False, verbose_name='Consent to Share Presentation Materials With Club Members'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='consent_streaming',
            field=models.BooleanField(default=False, verbose_name='Consent to Upload Recordings to Streaming Platform(s)'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='consent_video_rec',
            field=models.BooleanField(default=False, verbose_name='Consent to Record Video'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='length',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Presentation Length'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='topic',
            field=models.CharField(default='', max_length=250, verbose_name='Presentation Topic'),
        ),
        migrations.AlterField(
            model_name='guestspeakercontactform',
            name='visual_aids',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Prepared Visual Aids'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='availability_end',
            field=models.DateField(blank=True, null=True, verbose_name='End of Mentorship Availability'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='availability_start',
            field=models.DateField(verbose_name='Start of Mentorship Availability'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='field_description',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Field/Sector Name'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='field_name',
            field=models.CharField(default='', max_length=200, verbose_name='Field/Sector Name'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='field_type',
            field=models.CharField(default='', max_length=60, verbose_name='Type of Field'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='meeting_information',
            field=models.JSONField(default=list, validators=[core.validators.JSONSchemaValidator(limit_value={'items': {'additionalProperties': False, 'properties': {'time': {'format': 'time', 'title': 'Time Available', 'type': 'string'}, 'weekday': {'enum': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'title': 'Day of Week', 'type': 'string'}}, 'required': ['weekday', 'time'], 'title': 'Weekday/Time of Availability', 'type': 'object'}, 'minItems': 1, 'schema': 'http://json-schema.org/draft-07/schema#', 'title': 'Weekly Meeting Availability', 'type': 'array'})], verbose_name='Weekly Meeting Availability'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='students',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Number of students too small.'), django.core.validators.MaxValueValidator(6, 'Number of students too large.')], verbose_name='Number of Students to Mentor'),
        ),
        migrations.AlterField(
            model_name='mentorcontactform',
            name='weekly_minutes',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Number of minutes too small.')], verbose_name='Minutes of Availability Per Week'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='commercial',
            field=models.BooleanField(default=False, verbose_name='Commercial Organization?'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='funding',
            field=models.BooleanField(default=False, verbose_name='Willing/Able to Provide Funding for Club Initiatives'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='industry',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Industries'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='initiatives',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Club Initiatives to Provide Funding For'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='max_org_size',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Estimated Maximum Size of Organization'),
        ),
        migrations.AlterField(
            model_name='partnercontactform',
            name='min_org_size',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Estimated Minimum Size of Organization'),
        ),
    ]
