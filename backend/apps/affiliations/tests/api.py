"""This module contains unit tests for the affiliations application's API serializers and viewsets."""
from django.urls import reverse
from django.test import tag
from rest_framework import status

from apps.affiliations.models import Affiliate
from core.testcases import VerboseAPITestCase, Tags


class AffiliateEndpointTestCase(VerboseAPITestCase):
    """A test case class which contains unit tests for the Affiliate model API endpoint.
    """
    message = 'Testing Affiliate model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = SimpleUploadedFile('logo.png', b'file_content')

        cls.affiliate = Affiliate(
            name='Django Software Foundation',
            logo=image,
            website='https://www.djangoproject.com/foundation/',
        )
        cls.affiliate.save()

    @classmethod
    def tearDownClass(cls):
        """Delete the Affiliate model instance used for testing once all the test cases have been executed.

        This is necessary to ensure that the temporary image file created on the disk for the tests is deleted.
        """
        super().tearDownClass()
        if hasattr(cls, 'affiliate'):
            cls.affiliate.delete()

    # noinspection DuplicatedCode
    @tag(Tags.API)
    def test_read_only(self):
        """Ensure that the API endpoint for multiple Affiliate model instances is read-only.
        """
        url = reverse('affiliate-list')

        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{url}/{self.affiliate.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag(Tags.API)
    def test_logo_url_serializer_field(self):
        """Ensure that the `logo_url` serializer method field has the correct value in an API response.
        """
        url = reverse('affiliate-list')
        response = self.client.get(f'{url}/{self.affiliate.pk}/')

        self.assertEqual(self.affiliate.logo.url, response.data['logo_url'])
