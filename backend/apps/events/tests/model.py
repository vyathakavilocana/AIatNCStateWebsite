"""This module contains unit tests for the events application's Django models."""
from django.test import tag
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytz

from apps.events.models import Event, ContactInfo
from core.testcases import VerboseTestCase, Tags


class TestContactInfoModel(VerboseTestCase):
    """A Django test case class which contains unit tests for ContactInfo model functionality.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing ContactInfo model...'

    @classmethod
    def setUpTestData(cls):
        """Creates and saves a valid Event object for creating ContactInfo objects in individual tests.
        """
        cls.event = Event(
            type=Event.EventType.OTHER,
            topics=['Topic 1'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )
        cls.event.save()

    @tag(Tags.MODEL)
    def test_clean_email_type_valid_email(self):
        """Ensure that a ValidationError is not raised for an object with type `EMAIL` and a valid email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            event=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_email_type_invalid_email(self):
        """Ensure that a ValidationError is raised for an object with type `EMAIL` and an invalid email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='invalid.email',
            event=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_email_type__empty_value(self):
        """Ensure that a ValidationError is raised for an object with type `EMAIL` and an invalid (empty) email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='',
            event=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    '''
    @tag(Tags.MODEL)
    def test_clean_phone_type_valid_phone(self):
        """TODO Docs
        """
        pass

    @tag(Tags.MODEL)
    def test_clean_phone_type_invalid_phone(self):
        """TODO Docs
        """
        pass
    '''

    @tag(Tags.MODEL)
    def test_clean_other_type_valid_email(self):
        """Ensure that a ValidationError is not raised for an object with type `OTHER` and a valid email value.

        Additionally, ensure that the object's type was properly coerced to `EMAIL`, since its value was a valid email
        address.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value='valid@email.com',
            event=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)
        contact.save()
        self.assertEqual(ContactInfo.InfoType.EMAIL, contact.type)

    '''
    @tag(Tags.MODEL)
    def test_clean_other_type_valid_phone(self):
        """TODO Docs
        """
        pass

    @tag(Tags.MODEL)
    def test_clean_other_type_invalid_email_and_phone(self):
        """TODO Docs
        """
        pass
    '''


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
