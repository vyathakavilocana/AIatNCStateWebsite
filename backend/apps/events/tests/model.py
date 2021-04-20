"""This module contains unit tests for the events application's Django models."""
from django.test import tag
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytz

from apps.events.models import Event, ContactInfo
from core.testcases import VerboseTestCase, Tags


class TestContactInfoModel(VerboseTestCase):
    """TODO Docs
    """

    message = 'Testing ContactInfo model...'

    @classmethod
    def setUpTestData(cls):
        """TODO Docs
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
        """TODO Docs
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
        """TODO Docs
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='invalid.email',
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
        """TODO Docs
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
    """TODO Docs
    """

    message = 'Testing Event model...'

    @tag(Tags.JSON)
    def test_valid_topics_empty_list(self):
        """TODO Docs
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
        """TODO Docs
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
        """TODO Docs
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
        """TODO Docs
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=['Topic 1', ' '],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )

        self.assertRaises(ValidationError, event.full_clean)

    @tag(Tags.MODEL)
    def test_str_same_start_and_end_day(self):
        """TODO Docs
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
        """TODO Docs
        """
        event = Event(
            type=Event.EventType.OTHER,
            topics=[],
            start=timezone.datetime(2021, 4, 20, 1, 30, tzinfo=pytz.UTC),
            end=timezone.datetime(2021, 4, 21, 3, 30, tzinfo=pytz.UTC)
        )
        event.save()

        self.assertEqual(f'{Event.EventType.OTHER.label} from 04-20-2021 to 04-21-2021', str(event))
