"""This module contains Django models that relate to club events."""
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from celery import current_app

from core.validators import JSONSchemaValidator


# A JSON schema used in validating the topics field of the Event model. This field is only valid if it contains a JSON
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


class EventQuerySet(models.QuerySet):
    """A custom QuerySet for the Event model which provides additional methods for retrieving Event objects.
    """
    def upcoming(self):
        """A custom queryset method which returns a queryset containing all upcoming events.

        Upcoming Events are those which have a start date and time that have yet to pass.
        """
        return self.all().filter(Q(start__gt=timezone.now()))


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
    # TODO: meeting_address = ...

    contacts = GenericRelation('core.ContactInfo')
    objects = EventQuerySet.as_manager()

    def save(self, *args, **kwargs):
        """Overrides the default model save method to send Celery tasks and include additional validation.

        TODO Update related announcement object when event saved.
        """
        # Ensure that the event's start date/time comes before its end date/time.
        if self.start >= self.end:
            raise ValidationError('Event start date and time must fall before its end date and time.')

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
            return f'{self.EventType(self.type).label} from {self.start.strftime("%m-%d-%Y")} '\
                        + f'to {self.end.strftime("%m-%d-%Y")}'

    class Meta:
        """This class contains meta-options for the Event model.

        Attributes:  #noqa
            ordering: A list of fields to order Event objects by. As-is, they are ordered by the date/time they start
            and in ascending order (i.e., the Event that is starting the soonest appears first and the one starting
            latest appears last).
        """
        ordering = ['start']
