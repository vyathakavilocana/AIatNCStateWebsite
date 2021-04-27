"""This module contains unit tests for the affiliations application's Django models."""
from django.conf import settings
from django.test import tag
import os

from apps.affiliations.models import Affiliate, BASE_LOGO_PATH
from core.testcases import VerboseTestCase, Tags


class TestAffiliateModel(VerboseTestCase):
    """A test case class which contains unit tests for Affiliate model functionality.
    """
    message = 'Testing Affiliate model...'

    @classmethod
    def setUpTestData(cls):
        """Creates a generic image for creating Affiliate objects in individual tests.
        """
        from django.core.files.uploadedfile import SimpleUploadedFile

        cls.image = SimpleUploadedFile('logo.png', b'file_content')

    @tag(Tags.MODEL)
    def test_logo_file_deleted_with_object(self):
        """Ensure that an affiliate's logo is deleted from the disk when its associated Affiliate object is deleted.
        """
        affiliate = Affiliate(
            name='Django Software Foundation',
            logo=self.image,
            website='https://www.djangoproject.com/foundation/',
        )
        affiliate.save()

        path = f'{affiliate.logo.path}'
        affiliate.delete()

        if os.path.isfile(path):
            self.fail('Logo image file was not deleted along with the model instance.')

    @tag(Tags.MODEL)
    def test_logo_path_properly_assigned(self):
        """Ensure that the URL and name of an affiliate's logo are properly assigned when creating an Affiliate object.
        """
        affiliate = Affiliate(
            name='JetBrains',
            logo=self.image,
            website='https://www.python.org/psf-landing/',
        )
        affiliate.save()

        try:
            self.assertEqual(affiliate.logo.url, f'{settings.MEDIA_URL}{BASE_LOGO_PATH}jetbrains.png')
        except AssertionError as e:
            affiliate.delete()
            self.fail(e)

        affiliate.delete()

    @tag(Tags.MODEL)
    def test_affiliate_string_representation(self):
        """Ensure that the string representation of an affiliate instance simply contains the affiliate's name as-is.
        """
        affiliate = Affiliate(
            name='Google',
            logo=self.image,
            website='https://www.google.com',
        )
        affiliate.save()

        try:
            self.assertEqual(str(affiliate), 'Google')
        except AssertionError as e:
            affiliate.delete()
            self.fail(e)

        affiliate.delete()
