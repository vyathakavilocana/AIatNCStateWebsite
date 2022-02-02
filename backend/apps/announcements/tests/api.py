"""This module contains unit tests for the announcements application's API serializers and viewsets."""
from django.urls import reverse
from django.test import tag
from rest_framework import status

from core.testcases import VerboseAPITestCase, Tags
from apps.announcements.models import Announcement


class AnnouncementEndpointTestCase(VerboseAPITestCase):
    """TODO Docs
    """
    message = 'Testing Announcement model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.announcement = Announcement(
            title='Announcement Title',
            body=[
                {
                    'element': 'h3',
                    'content': 'Header Text'
                },
                {
                    'element': 'hr'
                },
                {
                    'element': 'p',
                    'content': 'Paragraph text content'
                }
            ]
        )
        cls.announcement.save()

    @tag(Tags.API)
    def test_read_only(self):
        """Ensure that the API endpoint for multiple Announcement model instances is read-only.
        """
        url = reverse('announcement-list')

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

        response = self.client.get(f'{url}/{self.announcement.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag(Tags.API)
    def test_created_serializer_method_field(self):
        """Ensure that the `created` serializer method field has the correct keys/values in an API response.
        """
        url = reverse('announcement-list')

        response = self.client.get(f'{url}/{self.announcement.pk}/')
        created = response.data['created']

        self.assertTrue('date' in created)
        self.assertEqual(self.announcement.created.strftime('%m-%d-%Y'), created['date'])

        self.assertTrue('time' in created)
        self.assertEqual(self.announcement.created.strftime('%I:%M %p'), created['time'])

    @tag(Tags.API)
    def test_list_action_invalid_count_negative(self):
        """Ensure that specifying a negative count causes an API response with the 'bad request' status code.
        """
        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=-1')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @tag(Tags.API)
    def test_list_action_invalid_count_zero(self):
        """Ensure that specifying a count of zero causes an API response with the 'bad request' status code.
        """
        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=0')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @tag(Tags.API)
    def test_list_action_invalid_count_non_integer(self):
        """Ensure that specifying a non-integer count causes an API response with the 'bad request' status code.
        """
        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=a')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @tag(Tags.API)
    def test_list_action_valid_count_less_than_num_in_db(self):
        """Ensure that specifying a valid count does not cause any issues.
        """
        e = Announcement(
            title='Second Announcement',
            body=[{'element': 'hr'}]
        )
        e.save()

        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))

    @tag(Tags.API)
    def test_list_action_valid_count_equal_to_num_in_db(self):
        """Ensure that specifying a valid count does not cause any issues.
        """
        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))

    @tag(Tags.API)
    def test_list_action_valid_count_greater_than_num_in_db(self):
        """Ensure that specifying a valid count does not cause any issues.
        """
        url = reverse('announcement-list')
        response = self.client.get(f'{url}?count=2')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
