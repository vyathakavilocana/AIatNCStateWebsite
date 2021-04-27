"""This module contains unit tests for the events application's API serializers and viewsets."""
from datetime import timedelta

from django.urls import reverse
from django.test import tag
from django.utils import timezone
from rest_framework import status

from apps.events.models import Event, ContactInfo
from core.testcases import VerboseAPITestCase, Tags


class EventEndpointTestCase(VerboseAPITestCase):
    """A test case class which contains unit tests for the Event model API endpoint.
    """
    message = 'Testing Event model API endpoint'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['Autoencoders', 'Gradient boosting'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2),
            calendar_link='https://www.google.com',
            meeting_link='https://www.google.com',
        )
        cls.event.save()

        cls.contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            event=cls.event
        )
        cls.contact.save()

    # noinspection DuplicatedCode
    @tag(Tags.API)
    def test_read_only(self):
        """Ensure that the API endpoint for multiple Event model instances is read-only.
        """
        url = reverse('event-list')

        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'{url}/{self.event.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag(Tags.API)
    def test_event_type_serializer_method_field(self):
        """Ensure that the event `type` serializer method field has the correct value in an API response.
        """
        url = reverse('event-list')

        response = self.client.get(f'{url}/{self.event.pk}/')
        self.assertEqual(Event.EventType(self.event.type).label, response.data['type'])

    @tag(Tags.API)
    def test_event_start_serializer_method_field(self):
        """Ensure that the `start` serializer method field has the correct keys/values in an API response.
        """
        url = reverse('event-list')

        response = self.client.get(f'{url}/{self.event.pk}/')
        start = response.data['start']

        self.assertTrue('date' in start)
        self.assertEqual(self.event.start.strftime('%m-%d-%Y'), start['date'])

        self.assertTrue('time' in start)
        self.assertEqual(self.event.start.strftime('%I:%M %p'), start['time'])

    @tag(Tags.API)
    def test_event_end_serializer_method_field(self):
        """Ensure that the `end` serializer method field has the correct keys/values in an API response.
        """
        url = reverse('event-list')

        response = self.client.get(f'{url}/{self.event.pk}/')
        end = response.data['end']

        self.assertTrue('date' in end)
        self.assertEqual(self.event.end.strftime('%m-%d-%Y'), end['date'])

        self.assertTrue('time' in end)
        self.assertEqual(self.event.end.strftime('%I:%M %p'), end['time'])

    @tag(Tags.API)
    def test_contact_info_type_serializer_method_field(self):
        """Ensure that the contact info `type` serializer method field has the correct value in an API response.
        """
        url = reverse('event-list')

        response = self.client.get(f'{url}/{self.event.pk}/')
        contact = response.data['contacts'][0]

        self.assertEqual(ContactInfo.InfoType(self.contact.type).label, contact['type'])
