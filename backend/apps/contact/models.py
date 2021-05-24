"""TODO Docs"""
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from polymorphic.models import PolymorphicModel

from core.validators import JSONSchemaValidator

GUEST_SPEAKER_AVAILABILITY_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Availability',
    'type': 'array',
    'minItems': 1,
    'maxItems': 3,
    'items': {
        'title': 'Date/Time of Availability',
        'properties': {
            'date': {
                'title': 'Date',
                'type': 'string',
                'format': 'date'
            },
            'time': {
                'title': 'Time',
                'type': 'string',
                'format': 'time'
            }
        },
        'required': ['date', 'time'],
        'additionalProperties': False
    }
}

MENTOR_MEETING_INFORMATION_FIELD_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Weekly Meeting Availability',
    'type': 'array',
    'minItems': 1,
    'items': {
        'title': 'Weekday/Time of Availability',
        'type': 'object',
        'properties': {
            'weekday': {
                'title': 'Day of Week',
                'type': 'string',
                'enum': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            },
            'time': {
                'title': 'Time Available',
                'type': 'string',
                'format': 'time'
            }
        },
        'required': ['weekday', 'time'],
        'additionalProperties': False
    }
}


class ContactFormBase(PolymorphicModel):
    """TODO Docs
    """
    first_name = models.CharField(
        max_length=80,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=80,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Last Name',
    )
    affiliation = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Affiliate Organization',
    )
    contacts = GenericRelation('core.ContactInfo')
    thoughts = models.TextField(
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Additional Thoughts/Questions/Concerns',
    )
    submitted = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Date/Time Submitted'
    )
    reviewed = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Form Reviewed?',
    )
    ignored = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Ignored?',
    )
    comments = GenericRelation('contact.AdminComment')

    def __str__(self):
        """TODO Docs
        """
        return f'{self.first_name} {self.last_name} - {self.submitted.strftime("%m-%d-%Y")}'

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Submitted Contact Form'
        ordering = ['-submitted']


class GuestSpeakerContactForm(ContactFormBase):
    """TODO Docs
    """
    topic = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Presentation Topic',
    )
    availability = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=GUEST_SPEAKER_AVAILABILITY_FIELD_SCHEMA)],
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Availability',
    )
    length = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Presentation Length',
    )
    visual_aids = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Prepared Visual Aids',
    )
    addl_visual_aids = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Additional Visual Aids Required',
    )
    addl_tech = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Additional Tech Setup Required',
    )
    consent_audio_rec = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Consent to Record Audio',
    )
    consent_video_rec = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Consent to Record Video',
    )
    consent_streaming = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Consent to Upload Recordings to Streaming Platform(s)',
    )
    consent_materials = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Consent to Share Presentation Materials With Club Members',
    )

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Guest Speaker Contact Form'


class MentorContactForm(ContactFormBase):
    """TODO Docs
    """
    students = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Number of Students to Mentor',
        validators=[
            MinValueValidator(1, 'Number of students too small.'),
            MaxValueValidator(6, 'Number of students too large.'),
        ],
    )
    field_type = models.CharField(
        max_length=60,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Type of Field',
    )
    field_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Field/Sector Name',
    )
    field_description = models.TextField(
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Field/Sector Name',
    )
    availability_start = models.DateField(
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Start of Mentorship Availability',
    )
    availability_end = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='End of Mentorship Availability',
    )
    meeting_information = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=MENTOR_MEETING_INFORMATION_FIELD_SCHEMA)],
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Weekly Meeting Availability',
    )
    weekly_minutes = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Minutes of Availability Per Week',
        validators=[
            MinValueValidator(1, 'Number of minutes too small.'),
        ],
    )

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Mentor Contact Form'


class EventOrganizerContactForm(ContactFormBase):
    """TODO Docs

    TODO Validation for min/max attendees
    """
    event_type = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Type of Event to Organize',
    )
    financial_assistance = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Financial Assistance from Club Required?',
    )
    min_attendees = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Estimated/Desired Minimum Number of Attendees',
    )
    max_attendees = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Estimated/Desired Maximum Number of Attendees',
    )
    advertising = models.TextField(
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Event Advertising Campaign Information',
    )

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Event Organizer Contact Form'


class PartnerContactForm(ContactFormBase):
    """TODO Docs

    TODO Validation for min/max organization size.
    """
    commercial = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Commercial Organization?',
    )
    industry = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Industries',
    )
    min_org_size = models.PositiveIntegerField(
        null=True,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Estimated Minimum Size of Organization',
    )
    max_org_size = models.PositiveIntegerField(
        null=True,
        blank=False,
        default=1,
        editable=True,
        unique=False,
        verbose_name='Estimated Maximum Size of Organization',
    )
    funding = models.BooleanField(
        default=False,
        editable=True,
        verbose_name='Willing/Able to Provide Funding for Club Initiatives',
    )
    initiatives = models.TextField(
        null=True,
        blank=True,
        default='',
        editable=True,
        unique=False,
        verbose_name='Club Initiatives to Provide Funding For',
    )

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Partner Contact Form'


class AdminComment(models.Model):
    """TODO Docs

    # TODO Validation to ensure non-admin users can't create admin comments.
    # TODO Validation to ensure that form_type is actually one of the contact form models.
    """
    first_name = models.CharField(
        max_length=80,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=80,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Last Name',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Time/Date Comment Added'
    )

    form_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_query_name='comments'
    )
    form_id = models.PositiveIntegerField()
    form = GenericForeignKey('form_type', 'form_id')

    class Meta:
        """TODO Docs
        """
        verbose_name = 'Administrator Comment'
