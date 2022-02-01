"""TODO Docs"""
from unittest.mock import patch

from django.test import tag

from core.testcases import VerboseTestCase, Tags
from apps.projects.models import Project


class TestProjectsTasks(VerboseTestCase):
    """TODO Docs
    """
    message = 'Testing projects app tasks...'

    @tag(Tags.TASK)
    @patch('apps.projects.tasks.project_created.delay')
    def test_project_created(self, project_created):
        """TODO Docs
        """
        project = Project(
            name='Test Project',
            authors=['Author 1'],
            description='Project description.',
            status=Project.ProjectStatus.PLANNED
        )
        project.save()

        self.assertTrue(project_created.called)
        self.assertEqual(project.name, project_created.call_args[0][0])
        self.assertEqual(project.authors, project_created.call_args[0][1])
        self.assertEqual(project.description, project_created.call_args[0][2])
        self.assertEqual(project.url, project_created.call_args[0][3])
