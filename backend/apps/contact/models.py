"""This module contains Django models that relate to contact forms."""
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from polymorphic.models import PolymorphicModel

from core.validators import JSONSchemaValidator


# A JSON schema used in validating the `availability` field of the GuestSpeakerContactForm model. This field is only
# valid if it contains a JSON array with 1-3 objects containing string properties representing the date(s) and time(s)
# when the guest speaker would be available to present.
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

# A JSON schema used in validating the `meeting_information` field of the MentorContactForm model. This field is only
# valid if it contains a JSON array with one or more objects containing string properties which represent the weekday(s)
# and time(s) when the mentor would be available to meet.
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
    """A base model from which concrete contact form model classes inherit the basic fields required in all contact
    form submissions.
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
        """Defines the string representation of a contact form model to be the first and last name of the form's
        submitter, followed by the date when the form was submitted.
        """
        return f'{self.first_name} {self.last_name} - {self.submitted.strftime("%m-%d-%Y")}'

    class Meta:
        """Defines the long-form name to label contact forms as well as the order in which they should appear when
        queried from the database.
        """
        verbose_name = 'Submitted Contact Form'
        ordering = ['-submitted']


class GuestSpeakerContactForm(ContactFormBase):
    """A concrete contact form model, intended for prospective guest speakers, which includes additional information
    such as the presentation topic and length, speaker availability, accommodations needed, and consent fields for
    audio/video recordings of the meeting.
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
        """Defines the long-form name to label GuestSpeakerContactForm objects.
        """
        verbose_name = 'Guest Speaker Contact Form'


class MentorContactForm(ContactFormBase):
    """A concrete contact form model, intended for prospective mentors, which includes additional information
    such as the number of students to mentor, information about the mentor's background and field of expertise, and
    the availability of the prospective mentor to meet with club members.
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
        """Defines the long-form name to label MentorContactForm objects.
        """
        verbose_name = 'Mentor Contact Form'


class EventOrganizerContactForm(ContactFormBase):
    """A concrete contact form model, intended for event organizers, which includes additional information
    such as the type of event, expected attendance, and financial/advertising information.
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
        validators=[
            MinValueValidator(1, 'Estimated minimum number of attendees too small.'),
        ],
    )
    max_attendees = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        default=2,
        editable=True,
        unique=False,
        verbose_name='Estimated/Desired Maximum Number of Attendees',
        validators=[
            MinValueValidator(2, 'Estimated maximum number of attendees too small.'),
        ],
    )
    advertising = models.TextField(
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Event Advertising Campaign Information',
    )

    def clean(self):
        """Provides additional validation for EventOrganizerContactForm model fields.

        Raises a ValidationError if both `min_attendees` and `max_attendees` are not none and `min_attendees` is greater
        than `max_attendees`.
        """
        if not (self.min_attendees is None or self.max_attendees is None) and self.min_attendees > self.max_attendees:
            raise ValidationError('Minimum number of attendees must not be greater than maximum number of attendees')

    class Meta:
        """Defines the long-form name to label EventOrganizerContactForm objects.
        """
        verbose_name = 'Event Organizer Contact Form'


class PartnerContactForm(ContactFormBase):
    """A concrete contact form model, intended for club partners, which includes additional information
    such as the type, industry, and size of the organization, whether the organization is interested in funding the
    club, and the types of club's initiatives that the organization is interested in supporting.
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
        validators=[
            MinValueValidator(1, 'Estimated minimum number of employees too small.'),
        ],
    )
    max_org_size = models.PositiveIntegerField(
        null=True,
        blank=False,
        default=2,
        editable=True,
        unique=False,
        verbose_name='Estimated Maximum Size of Organization',
        validators=[
            MinValueValidator(2, 'Estimated maximum number of employees too small.'),
        ],
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

    def clean(self):
        """Provides additional validation for PartnerContactForm model fields.

        Raises a ValidationError if both `min_org_size` and `max_org_size` are not None and `min_org_size` is greater
        than `max_org_size`.
        """
        if not (self.min_org_size is None or self.max_org_size is None) and self.min_org_size > self.max_org_size:
            raise ValidationError('Estimated minimum organization size must be less than estimated maximum '
                                  'organization size.')

    class Meta:
        """Defines the long-form name to label PartnerContactForm objects.
        """
        verbose_name = 'Partner Contact Form'


class AdminComment(models.Model):
    """A Django database model which represents a comment left by an administrator which pertains to a submitted contact
    form.
    """
    _SUPPORTED_RELATION_TYPES = (
        'GuestSpeakerContactForm', 'MentorContactForm', 'EventOrganizerContactForm', 'PartnerContactForm',
    )

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
    comment = models.TextField(
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Comment',
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

    def clean(self):
        """This method defines custom ContactInfo model validation logic.
        """
        if self.form.__class__.__name__ not in self._SUPPORTED_RELATION_TYPES:
            raise ValidationError(
                f'Unsupported form type "{type(self.form_type.__class__.__name__)}" supplied for '
                + 'GenericForeignKey relation.'
            )

    class Meta:
        """Defines the long-form name to label administrator comments.
        """
        verbose_name = 'Administrator Comment'
