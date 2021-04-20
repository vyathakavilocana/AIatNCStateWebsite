from django.core.exceptions import ValidationError
from django.test import tag

from apps.projects.models import Project
from core.testcases import VerboseTestCase, Tags


class TestProjectModel(VerboseTestCase):
    """TODO Docs
    """

    message = 'Testing Project model...'

    @tag(Tags.JSON)
    def test_valid_authors_one_author(self):
        """TODO Docs
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
        """TODO Docs
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
        """TODO Docs
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
        """TODO Docs
        """
        project = Project(
            name='Test Project',
            authors=['Author 1', ' '],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertRaises(ValidationError, project.full_clean)

    @tag(Tags.JSON)
    def test_invalid_authors_two_invalid(self):
        """TODO Docs
        """
        project = Project(
            name='Test Project',
            authors=['', ' '],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )

        self.assertRaises(ValidationError, project.full_clean)
