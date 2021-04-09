from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.validators import JSONSchemaValidator


# TODO Docs
EVENT_TOPICS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Event Topics',
    'description': 'A list of topics (as strings) for an event.',
    'type': 'array',
    'properties': {
        'items': {
            'type': 'string'
        }
    }
}


class ContactInfo(models.Model):
    """
    TODO Docs
    """

    class InfoType(models.TextChoices):
        """
        TODO Docs
        """
        EMAIL = 'EM', _('Email')
        PHONE = 'PH', _('Phone')
        OTHER = 'OT', _('Other')

    type = models.CharField(
        max_length=2,
        choices=InfoType.choices,
        default=InfoType.EMAIL,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Contact Information Type'
    )
    preferred = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Preferred Method of Contact',
    )
    value = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Contact Value',
        # validators=  TODO
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        editable=True,
        verbose_name='Associated Event',
        related_name='contacts',
        db_constraint=True,
    )


class Event(models.Model):
    """
    TODO Docs
    """

    class EventType(models.TextChoices):
        """
        TODO Docs
        """
        GUEST_SPEAKER = 'GS', _('Guest Speaker Presentation')
        WORKSHOP = 'WS', _('Workshop')
        INTERVIEW_PREP = 'IP', _('Interview Prep Session')
        DISCUSSION = 'DI', _('Free Form Discussion')
        PROJECT_MEETING = 'PM', _('Group Project Meeting')
        HACKATHON_MEETING = 'HM', _('Hackathon Meeting')
        OTHER = 'OT', _('Other')

    type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.OTHER,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Type of Event'
    )
    topics = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=EVENT_TOPICS_FIELD_JSON_SCHEMA)],
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Event Topics'
    )
    start = models.DateTimeField(
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Start Date and Time'
    )
    end = models.DateTimeField(
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='End Date and Time'
    )
    calendar_link = models.URLField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Calendar Invite Link',
        max_length=400
    )
    meeting_link = models.URLField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Virtual Meeting Link'
    )
    # TODO
    '''
    meeting_address = ...
    '''
