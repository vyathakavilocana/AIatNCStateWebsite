"""This module contains unit tests for the announcement application's Django models."""
from django.test import tag

from core.testcases import VerboseTestCase, Tags
from apps.announcements.models import Announcement


class TestAnnouncementModel(VerboseTestCase):
    """TODO Docs
    """
    message = 'Testing Announcement model...'

    @tag(Tags.MODEL)
    def test_str(self):
        """Ensure that an Announcement object's string representation is simply its title.
        """
        announcement = Announcement(
            title='Title'
        )
        announcement.save()

        self.assertEqual(announcement.title, str(announcement))

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_body_empty_list(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_body_object_no_props(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_body_valid_and_invalid_object(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_body_valid_object(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_body_valid_objects(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_hr(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h(self):
        """
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_a(self):
        """
        """
        self.not_implemented()
