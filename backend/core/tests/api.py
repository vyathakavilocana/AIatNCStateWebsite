"""This module contains unit tests for core application serializers and viewsets."""
from datetime import timedelta

from django.urls import reverse
from django.test import tag
from django.utils import timezone

from core.testcases import VerboseAPITestCase, Tags
from core.models import ContactInfo
from apps.events.models import Event


class ContactInfoEndpointTestCase(VerboseAPITestCase):
    """A test case class which contains unit tests for the ContactInfo model API endpoint.
    """
    message = 'Testing ContactInfo model API endpoint...'

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
            content_object=cls.event
        )
        cls.contact.save()

    @tag(Tags.API)
    def test_contact_info_type_serializer_method_field(self):
        """Ensure that the contact info `type` serializer method field has the correct value in an API response.
        """
        url = reverse('event-list')

        response = self.client.get(f'{url}/{self.event.pk}/')
        contact = response.data['contacts'][0]

        self.assertEqual(ContactInfo.InfoType(self.contact.type).label, contact['type'])
