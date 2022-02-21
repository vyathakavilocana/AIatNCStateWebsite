"""This module contains unit tests for the projects application's API serializers and viewsets."""
from django.urls import reverse
from django.test import tag
from rest_framework import status

from apps.projects.models import Project
from core.testcases import VerboseAPITestCase, Tags


class ProjectEndpointTestCase(VerboseAPITestCase):
    """A test case class which contains unit tests for the Project model API endpoint.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing Project model API endpoint...'

    @classmethod
    def setUpTestData(cls):
        """Set up the test data for the test case once when the test case class is being prepared to run.
        """
        cls.project = Project(
            name='Test Project',
            authors=['Author 1', 'Author 2'],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )
        cls.project.save()

    # noinspection DuplicatedCode
    @tag(Tags.API)
    def test_read_only(self):
        """Ensure that the API endpoint for multiple Event model instances is read-only.
        """
        url = reverse('project-list')

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

        response = self.client.get(f'{url}/{self.project.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # noinspection PyUnresolvedReferences
    @tag(Tags.API)
    def test_image_url_serializer_method_field(self):
        """Ensure that the `image_url` serializer method field has the correct value in an API response.
        """
        from django.core.files.uploadedfile import SimpleUploadedFile
        image = SimpleUploadedFile('logo.png', b'file_content')

        self.project.image = image
        self.project.save()

        url = reverse('project-list')
        response = self.client.get(f'{url}/{self.project.pk}/')

        try:
            self.assertEqual(self.project.image.url, response.data['image_url'])
        except AssertionError as e:
            self.project.image.delete()
            self.project.save()
            self.fail(e)

        self.project.image.delete()
        self.project.save()

    @tag(Tags.API)
    def test_image_url_serializer_method_field_no_image(self):
        """Ensure that the `image_url` serializer method field produces an empty string when the project has no image.
        """
        self.project.image = None
        self.project.save()

        url = reverse('project-list')
        response = self.client.get(f'{url}/{self.project.pk}/')

        self.assertEqual('', response.data['image_url'])

    @tag(Tags.API)
    def test_status_serializer_method_field(self):
        """Ensure that the project `status` serializer method field has the correct value in an API response.
        """
        url = reverse('project-list')

        response = self.client.get(f'{url}/{self.project.pk}/')
        self.assertEqual(Project.ProjectStatus(self.project.status).label, response.data['status'])

    @tag(Tags.API)
    def test_modified_serializer_method_field(self):
        """Ensure that the `modified` serializer method field has the correct keys/values in an API response.
        """
        url = reverse('project-list')

        response = self.client.get(f'{url}/{self.project.pk}/')
        modified = response.data['modified']

        self.assertTrue('date' in modified)
        self.assertEqual(self.project.modified.strftime('%m-%d-%Y'), modified['date'])

        self.assertTrue('time' in modified)
        self.assertEqual(self.project.modified.strftime('%I:%M %p'), modified['time'])
