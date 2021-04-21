"""This module contains Django models that relate to club events."""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

from core.validators import JSONSchemaValidator


# A JSON schema used in validating the topics field of the Event model. This field is only valid if it contains a JSON
# array whose elements are strings that are not empty and that do not only contain whitespace. Since some events may
# not have specific topics (e.g., hackathons), the array can be empty.
EVENT_TOPICS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Event Topics',
    'description': 'A list of topics (as strings) for an event.',
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)'
    }
}


class ContactInfo(models.Model):
    """A Django database model which represents a point of contact for a club event.

    In the PostgreSQL database, information for a method of contact has a type (email/phone/other), a field representing
    whether or not the method of contact is preferred, the actual value of the method of contact, and a many-to-one
    relationship to the Event model.

    Attributes:  # noqa
        type: A CharField containing the type of contact form. The available types are defined in the InfoType class.

        preferred: A BooleanField representing whether or not the contact method is a preferred method of contact.

        value: A CharField containing the actual value of the method of contact, whether that is a phone number, email
        address, or otherwise.

        event: A ForeignKey containing the primary key of the Event model instance that a ContactInfo model instance is
        related to. This is a many-to-one relationship, so any number of ContactInfo model instances can be related to
        a single Event model instance.
    """

    class InfoType(models.TextChoices):
        """Defines the supported types of contact information for the ContactInfo model's ``type`` field.

        Attributes:  # noqa
            EMAIL: A 2 character identifier and lazily-evaluated label representing the choice of an email address.

            PHONE: A 2 character identifier and lazily-evaluated label representing the choice of a phone number.

            OTHER: A 2 character identifier and lazily-evaluated label representing the catch-all choice for all other
            forms of contact.
        """
        EMAIL = 'EM', _('Email Address')
        PHONE = 'PH', _('Phone Number')
        OTHER = 'OT', _('Other Form of Contact')

    type = models.CharField(
        max_length=2,
        choices=InfoType.choices,
        default=InfoType.EMAIL,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Contact Information Type',
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

    def clean(self):
        """This method defines custom model validation logic.

        First, it validates a model instance's ``value`` field based upon its ``type`` (e.g., ``value`` is validated as
        a phone number if the instance's ``type`` is ``InfoType.PHONE``). Next, it attempts to coerce the value in a
        model instance's ``type`` field to the appropriate type based on its ``value`` field. That is, if a model
        instance's ``type`` field contains ``InfoType.OTHER``, but its ``value`` field contains a valid email address,
        the method will automatically set the instance's ``type`` field to ``InfoType.EMAIL``.
        """
        if self.type == self.InfoType.EMAIL:
            validate_email(self.value)
            return
        elif self.type == self.InfoType.PHONE:
            # TODO Validate phone number
            return

        valid_email = False
        try:
            validate_email(self.value)
            valid_email = True
        except ValidationError:
            pass

        if valid_email:
            self.type = self.InfoType.EMAIL
            return

        valid_phone = False
        # TODO Check if value is a valid phone number

        if valid_phone:
            self.type = self.InfoType.PHONE
            return


class Event(models.Model):
    """A Django database model which represents a club event.

    In the PostgreSQL database, a information for a method of contact has a type (email/phone/other), a field
    representing whether or not the method of contact is preferred, the actual value of the method of contact, and a
    many-to-one relationship to the Event model.

    Attributes:  # noqa
        type: A CharField containing the type of event. The available types are defined in the EventType class.

        topics: A JSONField containing a JSON representation of a list of topics for an event, if any.

        start: A DateTimeField containing the date and time of the start of the event.

        end: A DateTimeField containing the date and time of the end of the event.

        calendar_link: An optional URLField containing a calendar invite link to add the event to your calendar.

        meeting_link: An optional URLField containing a virtual meeting link to join an online, virtual meeting.

        meeting_address: TODO
    """

    class EventType(models.TextChoices):
        """Defines the supported types of events for the Event model's ``type`` field.

        Attributes:  # noqa
            GUEST_SPEAKER: A 2 character identifier and lazily-evaluated label representing the choice of a presentation
            by a guest speaker.

            WORKSHOP: A 2 character identifier and lazily-evaluated label representing the choice of a workshop.

            INTERVIEW_PREP: A 2 character identifier and lazily-evaluated label representing the choice of an interview
            preparation session.

            DISCUSSION: A 2 character identifier and lazily-evaluated label representing the choice of a free form
            discussion.

            PROJECT_MEETING: A 2 character identifier and lazily-evaluated label representing the choice of a group
            project meeting.

            HACKATHON_MEETING: A 2 character identifier and lazily-evaluated label representing the choice of a
            hackathon meeting.

            OTHER: A 2 character identifier and lazily-evaluated label representing the catch-all choice for all other
            types of events.
        """
        GUEST_SPEAKER = 'GS', _('Guest Speaker Presentation')
        WORKSHOP = 'WS', _('Workshop')
        INTERVIEW_PREP = 'IP', _('Interview Prep Session')
        DISCUSSION = 'DI', _('Free Form Discussion')
        PROJECT_MEETING = 'PM', _('Group Project Meeting')
        HACKATHON_MEETING = 'HM', _('Hackathon Meeting')
        OTHER = 'OT', _('Other Event')

    type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.OTHER,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Type of Event',
    )
    topics = models.JSONField(
        default=list,
        validators=[JSONSchemaValidator(limit_value=EVENT_TOPICS_FIELD_JSON_SCHEMA)],
        null=False,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Event Topics',
    )
    start = models.DateTimeField(
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Start Date and Time',
    )
    end = models.DateTimeField(
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='End Date and Time',
    )
    calendar_link = models.URLField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Calendar Invite Link',
        max_length=400,
    )
    meeting_link = models.URLField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name='Virtual Meeting Link',
    )
    # TODO
    '''
    meeting_address = ...
    '''

    def __str__(self):
        """Defines the string representation of the Event class.

        The string representation of an Event class instance contains the event type and the date(s) for which the event
        is scheduled. If the event occurs in a single day (i.e., its start and end dates are the same), only the start
        date is included. If the event occurs over the span of more than one day (i.e., its start and end dates are
        different), both the start and dates are included.

        Returns:
            A string containing the event's type and the date(s) when it is scheduled to occur.
        """
        if self.start.date() == self.end.date():
            return f'{self.EventType(self.type).label} on {self.start.strftime("%m-%d-%Y")}'
        else:
            return f'{self.EventType(self.type).label} from {self.start.strftime("%m-%d-%Y")} '\
                        + f'to {self.end.strftime("%m-%d-%Y")}'
