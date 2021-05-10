"""This module contains core functionality pertaining to test cases and unit testing in general."""
from enum import Enum
from typing import Type
from django.test import TestCase
from rest_framework.test import APITestCase


class Tags(Enum):
    """This enumeration defines various categories to tag unit tests with so that subsets of the unit tests can be run.

    Attributes:  # noqa
        JSON: A tag for unit tests that pertain to the use of JSON schemas.

        VALIDATION: A tag for unit tests that pertain to validation/validators.

        MODEL: A tag for unit tests that pertain to database models.

        API: A tag for unit tests that pertain to API functionality (e.g., serializers, viewsets).
    """
    JSON = 'jsonschema'
    VALIDATION = 'validation'
    MODEL = 'model'
    API = 'api'


# noinspection PyUnresolvedReferences
class VerboseTestCaseBase:
    """This class defines additional functionality for test case classes.

    It enables its subclasses to define a `message` attribute which is printed before running individual unit tests. It
    also includes helper methods which add to the existing assertion functionality of the Django TestCase class.
    """

    @classmethod
    def setUpClass(cls):
        """Checks if the class (or subclass) has a `message` attribute and prints it if so.
        """
        super().setUpClass()
        if hasattr(cls, 'message'):
            print('\n' + getattr(cls, 'message'))

    def assertStartsWith(self, first: str, second: str, message=None):
        """Assert that a string starts with another string.

        Args:
            first: The string to check for starting with the second string.
            second: The string to check for being the start of the first string.
            message: An optional message to print if the assertion fails.
        """
        self.assertTrue(first.startswith(second), message)

    def assertEndsWith(self, first: str, second: str, message=None):
        """Assert that a string ends with another string.

        Args:
            first: The string to check for ending with the second string.
            second: The string to check for being the end of the first string.
            message: An optional message to print if the assertion fails.
        """
        self.assertTrue(first.endswith(second), message)

    def assertNotRaises(self, expected_error: Type, call: callable, *args):
        """Assert that an error is not raised when calling a callable object.

        Args:
            expected_error: The error that is *not* supposed to be raised when the specified callable is called.
            call: The callable to call and check if the specified error is raised or not.
            *args: Optional, positional arguments to be passed to when calling the specified callable.
        """
        try:
            call(*args)
        except expected_error as e:
            self.fail(e)


class VerboseTestCase(VerboseTestCaseBase, TestCase):
    """A class which mixes verbose test case functionality with the built-in Django TestCase class.
    """


class VerboseAPITestCase(VerboseTestCaseBase, APITestCase):
    """A class which mixes verbose test case functionality with the built-in Django Rest Framework APITestCase class.
    """
