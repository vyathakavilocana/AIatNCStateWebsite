"""This module contains unit tests for the projects application's Django models."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import tag

from apps.projects.models import Project, BASE_IMAGE_PATH
from core.testcases import VerboseTestCase, Tags


class TestProjectModel(VerboseTestCase):
    """A Django test case class which contains unit tests for Project model functionality.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing Project model...'

    @classmethod
    def setUpTestData(cls):
        """Creates a generic image for creating Project objects in individual tests.
        """
        from django.core.files.uploadedfile import SimpleUploadedFile

        cls.image = SimpleUploadedFile('logo.png', b'file_content')

    @tag(Tags.JSON)
    def test_valid_authors_one_author(self):
        """Ensure that a ValidationError is not raised for an object with a list of authors containing one author.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1'],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertNotRaises(ValidationError, project.full_clean)

    @tag(Tags.JSON)
    def test_valid_authors_two_authors(self):
        """Ensure that a ValidationError is not raised for an object with a list of authors containing two authors.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', 'Author 2'],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertNotRaises(ValidationError, project.full_clean)

    @tag(Tags.JSON)
    def test_invalid_authors_empty_list(self):
        """Ensure that a ValidationError is raised for an object with an empty list of authors.
        """
        project = Project(
            name='Test Project',
            authors=[],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertRaises(ValidationError, project.full_clean)

    @tag(Tags.JSON)
    def test_invalid_authors_one_valid_one_invalid(self):
        """Ensure that a ValidationError is raised for an object with an invalid list of authors.

        A project author cannot be represented by a string of length zero.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', ''],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertRaises(ValidationError, project.full_clean)

    @tag(Tags.JSON)
    def test_invalid_authors_two_invalid(self):
        """Ensure that a ValidationError is raised for an object with an invalid list of authors.

        A project author cannot be represented by a string that only contains whitespace characters.
        """
        project = Project(
            name='Test Project',
            authors=['\t \r\n', ''],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertRaises(ValidationError, project.full_clean)

    @tag(Tags.MODEL)
    def test_image_file_deleted_with_object(self):
        """Ensure that a project's image is deleted from the disk when its associated Project object is deleted.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', 'Author 2'],
            description='Project description.',
            image=self.image,
            status=Project.ProjectStatus.PLANNED
        )
        project.save()

        path = f'{project.image.path}'
        project.delete()

        import os
        if os.path.isfile(path):
            self.fail('Project image file was not deleted along with the model instance.')

    @tag(Tags.MODEL)
    def test_logo_path_properly_assigned(self):
        """Ensure that the URL and name of a project's image are properly assigned when creating a Project object.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', 'Author 2'],
            description='Project description.',
            image=self.image,
            status=Project.ProjectStatus.PLANNED
        )
        project.save()

        try:
            self.assertEqual(f'{settings.MEDIA_URL}{BASE_IMAGE_PATH}test_project/main_image.png', project.image.url)
        except AssertionError as e:
            project.delete()
            self.fail(e)

        project.delete()

    @tag(Tags.MODEL)
    def test_project_string_representation(self):
        """Ensure that the string representation of a project object simply contains the project's name as-is.
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', 'Author 2'],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertEqual(project.name, str(project))
