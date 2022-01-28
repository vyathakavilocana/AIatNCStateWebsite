"""This module contains unit tests for the events application's Django models."""
from django.test import tag
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytz

from apps.events.models import Event, MeetingAddress
from core.testcases import VerboseTestCase, Tags


class TestMeetingAddressModel(VerboseTestCase):
    """A Django test case class which contains unit tests for MeetingAddress model functionality.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing MeetingAddress model...'

    @tag(Tags.MODEL)
    def test_valid_meeting_address(self):
        """Ensure that a ValidationError is not raised when cleaning a valid MeetingAddress object.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='Raleigh',
            state='NC',
            zip_code=27606,
            building_name='Hunt Library',
            room='Duke Energy Hall D'
        )

        self.assertNotRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_street_address(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `street_address`.
        """
        meeting_address = MeetingAddress(
            street_address='',
            city='Raleigh',
            state='NC',
            zip_code=27606,
            building_name='Hunt Library',
            room='Duke Energy Hall D'
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_city(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `city`.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='',
            state='NC',
            zip_code=27606,
            building_name='Hunt Library',
            room='Duke Energy Hall D'
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_state(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `state`.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='Raleigh',
            state='',
            zip_code=27606,
            building_name='Hunt Library',
            room='Duke Energy Hall D'
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)

        meeting_address.state = 'QX'
        self.assertRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_zip_code(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `zip_code`.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='Raleigh',
            state='NC',
            zip_code=9999,
            building_name='Hunt Library',
            room='Duke Energy Hall D'
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)

        meeting_address.zip_code = 270000
        self.assertRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_building_name(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `building_name`.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='Raleigh',
            state='NC',
            zip_code=27606,
            building_name='',
            room='Duke Energy Hall D'
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)

    @tag(Tags.MODEL)
    def test_invalid_room(self):
        """Ensure a ValidationError is raised when cleaning a MeetingAddress object with an invalid `room`.
        """
        meeting_address = MeetingAddress(
            street_address='1070 Partners Way',
            city='Raleigh',
            state='NC',
            zip_code=27606,
            building_name='Hunt Library',
            room=''
        )

        self.assertRaises(ValidationError, meeting_address.full_clean)


class TestEventModel(VerboseTestCase):
    """A Django test case class which contains unit tests for Event model functionality.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing Event model...'

    @tag(Tags.JSON)
    def test_valid_topics_empty_list(self):
        """Ensure that a ValidationError is not raised for an object with an empty list of topics.
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=[],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertNotRaises(ValidationError, event.full_clean)

    @tag(Tags.JSON)
    def test_valid_topics_nonempty_list(self):
        """Ensure that a ValidationError is not raised for an object with a list of topics containing one valid topic.
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=['Topic 1'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertNotRaises(ValidationError, event.full_clean)

    @tag(Tags.JSON)
    def test_invalid_topics_empty_string_in_list(self):
        """Ensure that a ValidationError is raised for an object with a single, invalid topic in its list of topics.

        Topics cannot be represented by strings of length 0.
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=[''],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_start_and_end(self):
        """Ensure that a ValidationError is not raised for an object with valid start and end datetimes.
        """
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertNotRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_end_datetime_before_start_datetime(self):
        """Ensure that a ValidationError is raised for an object whose start falls after its end.
        """
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now(),
            end=timezone.now() - timedelta(days=1)
        )

        self.assertRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_start_and_end_equal(self):
        """Ensure that a ValidationError is raised for an object whose start falls after its end.
        """
        time = timezone.now()
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=time,
            end=time
        )

        self.assertRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL)
    def test_queryset_no_upcoming_events(self):
        """Ensure that the `upcoming` method returns an empty queryset when there are no upcoming events.
        """
        e1 = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now() - timedelta(hours=1, days=1),
            end=timezone.now() - timedelta(days=1)
        )
        e2 = Event(
            type=Event.EventType.GUEST_SPEAKER,
            topics=['AI/ML'],
            start=timezone.now() - timedelta(hours=2, days=1),
            end=timezone.now() - timedelta(hours=1, days=1)
        )

        e1.save()
        e2.save()
        self.assertEqual(0, len(Event.objects.upcoming()))

    @tag(Tags.MODEL)
    def test_queryset_one_upcoming_event_one_passed(self):
        """Ensure that the `upcoming` method returns a queryset of length one when there is one upcoming event.
        """
        e1 = Event(
            type=Event.EventType.HACKATHON_MEETING,
            topics=['AI/ML'],
            start=timezone.now() + timedelta(hours=1, days=1),
            end=timezone.now() + timedelta(days=1)
        )
        e2 = Event(
            type=Event.EventType.GUEST_SPEAKER,
            topics=['AI/ML'],
            start=timezone.now() - timedelta(hours=2, days=1),
            end=timezone.now() - timedelta(hours=1, days=1)
        )

        e1.save()
        e2.save()
        self.assertEqual(1, len(Event.objects.upcoming()))
        self.assertEqual(e1.pk, Event.objects.upcoming()[0].pk)

    @tag(Tags.MODEL)
    def test_queryset_two_upcoming_events(self):
        """Ensure that a queryset of length two is returned when there are two upcoming events in the database.
        """
        e1 = Event(
            type=Event.EventType.PROJECT_MEETING,
            topics=['AI/ML'],
            start=timezone.now() + timedelta(hours=1, days=1),
            end=timezone.now() + timedelta(days=1)
        )
        e2 = Event(
            type=Event.EventType.GUEST_SPEAKER,
            topics=['AI/ML'],
            start=timezone.now() + timedelta(hours=2, days=1),
            end=timezone.now() + timedelta(hours=1, days=1)
        )

        e1.save()
        e2.save()
        self.assertEqual(2, len(Event.objects.upcoming()))

    @tag(Tags.MODEL)
    def test_queryset_event_in_progress(self):
        """Ensure that an event that has started, but not completed, is not included in the `upcoming` queryset.
        """
        e = Event(
            type=Event.EventType.WORKSHOP,
            topics=['Topic'],
            start=timezone.now() - timedelta(hours=1),
            end=timezone.now() + timedelta(hours=1)
        )

        e.save()
        self.assertEqual(0, len(Event.objects.upcoming()))

    @tag(Tags.JSON)
    def test_invalid_topics_whitespace_string_in_list_with_valid_string(self):
        """Ensure that a ValidationError is raised for an object with one valid and invalid topic in its list of topics.

        Topics cannot be represented by strings containing only whitespace characters.
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=['Topic 1', ' \t\f'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL)
    def test_str_same_start_and_end_day(self):
        """Ensure that an object's string representation is correct when its start and end dates are the same.

        An Event that starts and ends on the same day should have a string representation of the form:
        'EVENT_TYPE_LABEL on MM-DD-YYYY'
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=[],
            start=timezone.datetime(2021, 4, 20, 1, 30, tzinfo=pytz.UTC),
            end=timezone.datetime(2021, 4, 20, 3, 30, tzinfo=pytz.UTC)
        )
        event.save()

        self.assertEqual(f'{Event.EventType.OTHER.label} on 04-20-2021', str(event))

    @tag(Tags.MODEL)
    def test_str_different_start_and_end_day(self):
        """Ensure that an object's string representation is correct when its start and end dates are different.

        An Event that starts and ends on different days should have a string representation of the form:
        'EVENT_TYPE_LABEL from MM-DD-YYYY to MM-DD-YYYY'
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=[],
            start=timezone.datetime(2021, 4, 20, 1, 30, tzinfo=pytz.UTC),
            end=timezone.datetime(2021, 4, 21, 3, 30, tzinfo=pytz.UTC)
        )
        event.save()

        self.assertEqual(f'{Event.EventType.OTHER.label} from 04-20-2021 to 04-21-2021', str(event))
