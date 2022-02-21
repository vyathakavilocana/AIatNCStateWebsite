"""This module contains unit tests for the events application's Celery tasks."""
from datetime import timedelta
from unittest.mock import patch

from django.test import tag
from django.utils import timezone

from core.testcases import VerboseTestCase, Tags
from apps.events.models import Event


class TestEventsTasks(VerboseTestCase):
    """A Django test case class which contains unit tests for event-related Celery tasks.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing events app tasks...'

    @tag(Tags.TASK)
    @patch('apps.events.tasks.event_created.delay')
    def test_event_created(self, event_created):
        """Ensure that the `event_created` task is run with the correct arguments when a new Event object is created
        and saved.
        """
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )
        event.save()

        self.assertTrue(event_created.called)
        self.assertEqual(Event.EventType(event.type).label, event_created.call_args[0][0])
        self.assertEqual(event.start, event_created.call_args[0][1])

    @tag(Tags.TASK)
    @patch('apps.events.tasks.event_rescheduled.delay')
    def test_event_rescheduled(self, event_rescheduled):
        """Ensure that the `event_rescheduled` task is run with the correct arguments when an existing Event object is
        saved.
        """
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )
        event.save()

        event.start = timezone.now() + timedelta(days=1)
        event.save()

        self.assertTrue(event_rescheduled.called)
        self.assertEqual(Event.EventType(event.type).label, event_rescheduled.call_args[0][0])
        self.assertEqual(event.start, event_rescheduled.call_args[0][1])
