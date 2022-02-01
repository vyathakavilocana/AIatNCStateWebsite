"""TODO Docs"""
from django.test import tag
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.contact.models import GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, \
    PartnerContactForm
from core.testcases import VerboseAPITestCase, Tags


class GuestSpeakerContactFormEndpointTest(VerboseAPITestCase):
    """TODO Docs
    """
    message = 'Testing GuestSpeakerContactForm model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.form = GuestSpeakerContactForm(
            first_name='John',
            last_name='Smith',
            topic='AI/ML',
            length=90,
            availability=[
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'}
            ]
        )
        cls.form.save()

    @tag(Tags.API)
    def test_post_only(self):
        """Ensure that the endpoint only accepts post requests without logging in as an admin.
        """
        url = reverse('speaker-contact-form-list')

        response = self.client.post(url, data="""{
            "first_name": "John",
            "last_name": "Smith",
            "topic": "AI/ML",
            "length": 90,
            "availability": [
                {"date": "2018-11-13", "time": "20:20:39+00:00"},
                {"date": "2018-11-13", "time": "20:20:39+00:00"},
                {"date": "2018-11-13", "time": "20:20:39+00:00"}
            ],
            "contacts": [
                {"type": "EM", "preferred": true, "value": "test@gmail.com"}
            ]
        }""", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/{self.form.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MentorContactFormEndpointTest(VerboseAPITestCase):
    """TODO Docs
    """
    message = 'Testing MentorContactForm model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.form = MentorContactForm(
            first_name='John',
            last_name='Smith',
            students=4,
            field_type='Industry',
            field_name='AI/ML',
            availability_start=timezone.now(),
            weekly_minutes=90,
            meeting_information=[{'weekday': 'Monday', 'time': '18:00:00+00:00'}]
        )
        cls.form.save()

    @tag(Tags.API)
    def test_post_only(self):
        """Ensure that the endpoint only accepts post requests without logging in as an admin.
        """
        url = reverse('mentor-contact-form-list')

        response = self.client.post(url, data="""{
            "first_name": "John",
            "last_name": "Smith",
            "students": 4,
            "field_type": "Industry",
            "field_name": "AI/ML",
            "availability_start": "2022-12-20",
            "weekly_minutes": 90,
            "meeting_information": [
                {"weekday": "Monday", "time": "18:00:00+00:00"}
            ],
            "contacts": [
                {"type": "EM", "preferred": true, "value": "test@gmail.com"}
            ]
        }""", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/{self.form.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventOrganizerContactFormEndpointTest(VerboseAPITestCase):
    """TODO Docs
    """
    message = 'Testing EventOrganizerContactForm model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.form = EventOrganizerContactForm(
            first_name='John',
            last_name='Smith',
            event_type='Hackathon',
            advertising='Self-advertised',
            min_attendees=50,
            max_attendees=100
        )
        cls.form.save()

    @tag(Tags.API)
    def test_post_only(self):
        """Ensure that the endpoint only accepts post requests without logging in as an admin.
        """
        url = reverse('organizer-contact-form-list')

        response = self.client.post(url, data=f"""{{
            "first_name": "John",
            "last_name": "Smith",
            "event_type": "Hackathon",
            "advertising": "Self-advertised",
            "min_attendees": 50,
            "max_attendees": 100,
            "contacts": [
                {{"type": "EM", "preferred": true, "value": "test@gmail.com"}}
            ]
        }}""", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/{self.form.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PartnerContactFormEndpointTest(VerboseAPITestCase):
    """TODO Docs
    """
    message = 'Testing PartnerContactForm model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.form = PartnerContactForm(
            first_name='John',
            last_name='Smith',
            min_org_size=100,
            max_org_size=1000
        )
        cls.form.save()

    @tag(Tags.API)
    def test_post_only(self):
        """Ensure that the endpoint only accepts post requests without logging in as an admin.
        """
        url = reverse('organizer-contact-form-list')

        response = self.client.post(url, data=f"""{{
            "first_name": "John",
            "last_name": "Smith",
            "min_org_size": 100,
            "max_org_size": 1000,
            "contacts": [
                {{"type": "EM", "preferred": true, "value": "test@gmail.com"}}
            ]
        }}""", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/{self.form.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
