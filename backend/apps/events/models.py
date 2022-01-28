"""This module contains Django models that relate to club events."""
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from celery import current_app

from core.validators import JSONSchemaValidator

# A list of tuples containing the choices for the MeetingAddress model's `state` field.
STATE_CHOICES = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
    ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'Washington D.C.'), ('DE', 'Delaware'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
    ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
    ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
    ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
    ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming')
]

# A JSON schema used in validating the `topics` field of the Event model. This field is only valid if it contains a JSON
# array whose elements are strings that are not empty and that do not only contain whitespace. Since some events may
# not have specific topics (e.g., hackathons), the array can be empty.
EVENT_TOPICS_FIELD_JSON_SCHEMA = {
    'schema': 'http://json-schema.org/draft-07/schema#',
    'title': 'Event Topics',
    'type': 'array',
    'items': {
        'title': 'Topic',
        'type': 'string',
        'pattern': '(^(?!\\s*)$)|(^.*\\S.*$)'
    }
}


class MeetingAddress(models.Model):
    """TODO Docs

    Attributes:  # noqa
        street_address: A CharField containing the street address (first line) of the meeting address.

        city: A CharField containing the city where the address is located.

        state: A CharField containing the 2-letter abbreviation of the state where the address is located.

        zip_code: A PositiveIntegerField containing the address' zip code.

        building_name: A CharField containing the name of the building where an event is being held, if any.

        room: A CharField containing the room number/name where an event is being held.
    """
    street_address = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        editable=True,
        unique=True,
        verbose_name='Street Address',
    )
    city = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='City',
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='City',
    )
    zip_code = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=27606,
        editable=True,
        unique=False,
        verbose_name='Zip Code',
        validators=[
            MinValueValidator(10000, 'Zip code must contain 5 digits.'),
            MaxValueValidator(99999, 'Zip code must contain 5 digits.'),
        ],
    )
    building_name = models.CharField(
        max_length=75,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Building Name',
    )
    room = models.CharField(
        max_length=75,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Room Number/Name',
    )


class EventQuerySet(models.QuerySet):
    """A custom QuerySet for the Event model which provides additional methods for retrieving Event objects.
    """

    def upcoming(self):
        """A custom queryset method which returns a queryset containing all upcoming events.

        Upcoming Events are those which have a start date and time that have yet to pass.
        """
        return self.filter(Q(start__gt=timezone.now()))


class Event(models.Model):
    """A Django database model which represents a club event.

    Attributes:  # noqa
        type: A CharField containing the type of event. The available types are defined in the EventType class.

        topics: A JSONField containing a JSON representation of a list of topics for an event, if any.

        start: A DateTimeField containing the date and time of the start of the event.

        end: A DateTimeField containing the date and time of the end of the event.

        calendar_link: An optional URLField containing a calendar invite link to add the event to your calendar.

        meeting_link: An optional URLField containing a virtual meeting link to join an online, virtual meeting.

        meeting_address: TODO

        contacts: A generic relation to the ContactInfo model in the core directory.

        objects: A custom Manager which includes all base Manager functionality with the addition of the `upcoming`
        method which can be used in place of `Event.objects.all()` to retrieve a QuerySet containing only upcoming
        event objects.
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
    meeting_address = models.ForeignKey(
        MeetingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        editable=True,
        verbose_name='Meeting Location',
    )

    contacts = GenericRelation('core.ContactInfo')
    objects = EventQuerySet.as_manager()

    def clean(self):
        """Provides additional validation for Event model fields.

        Ensures that an Event object's start datetime must fall before its end datetime.
        """
        if self.start >= self.end:
            raise ValidationError('Event start date and time must fall before its end date and time.')

    def save(self, *args, **kwargs):
        """Overrides the default model save method to send a Celery task when a new Event object is saved.

        TODO Update related announcement object when event saved.
        """
        if self.pk:
            super(Event, self).save(*args, **kwargs)
            return

        super(Event, self).save(*args, **kwargs)
        current_app.send_task('apps.events.tasks.event_created_announcement', args=(self.pk,), countdown=5.)

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
            return f'{self.EventType(self.type).label} from {self.start.strftime("%m-%d-%Y")} ' \
                   + f'to {self.end.strftime("%m-%d-%Y")}'

    class Meta:
        """This class contains meta-options for the Event model.

        Attributes:  #noqa
            ordering: A list of fields to order Event objects by. As-is, they are ordered by the date/time they start
            and in ascending order (i.e., the Event that is starting the soonest appears first and the one starting
            latest appears last).
        """
        ordering = ['start']
