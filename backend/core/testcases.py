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

        TASK: A tag for unit tests that pertain to Celery tasks.
    """
    JSON = 'jsonschema'
    VALIDATION = 'validation'
    MODEL = 'model'
    API = 'api'
    TASK = 'task'


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

    def assertStartsWith(self, first: str, second: str, msg=None):
        """Assert that a string starts with another string.

        Args:
            first: The string to check for starting with the second string.
            second: The string to check for being the start of the first string.
            msg: An optional message to print if the assertion fails.
        """
        self.assertTrue(first.startswith(second), msg)

    def assertEndsWith(self, first: str, second: str, msg=None):
        """Assert that a string ends with another string.

        Args:
            first: The string to check for ending with the second string.
            second: The string to check for being the end of the first string.
            msg: An optional message to print if the assertion fails.
        """
        self.assertTrue(first.endswith(second), msg)

    def assertNotRaises(self, expected_error: Type, call: callable, *args, msg=None):
        """Assert that an error is not raised when calling a callable object.

        Args:
            expected_error: The error that is *not* supposed to be raised when the specified callable is called.
            call: The callable to call and check if the specified error is raised or not.
            *args: Optional, positional arguments to be passed when calling the specified callable.
            msg: An optional message to print if the assertion fails.
        """
        try:
            call(*args)
        except expected_error as e:
            if msg is not None:
                self.fail(f'{e}\n{msg}')
            else:
                self.fail(e)

    def assertWithDelete(self, obj, assertion: callable, *args, msg=None):
        """Check the specified assertion and delete the specified object, whether or not the assertion fails.

        Args:
            obj: The object to delete after checking whether the specified assertion holds or not. This should be an
            object of a model class.
            assertion: The assertion method to check. For example, `self.assertEquals`.
            *args: The positional arguments to pass to the specified assertion method
            msg: An optional message to print if the assertion fails.
        """
        try:
            assertion(*args)
            obj.delete()
        except AssertionError as e:
            obj.delete()
            if msg is not None:
                self.fail(f'{e}\n{msg}')
            else:
                self.fail(e)

    def not_implemented(self):
        """A convenience method, which fails a unit test, to be used when a test has yet to be implemented.
        """
        self.fail('Not yet implemented.')


class VerboseTestCase(VerboseTestCaseBase, TestCase):
    """A class which mixes verbose test case functionality with the built-in Django TestCase class.
    """


class VerboseAPITestCase(VerboseTestCaseBase, APITestCase):
    """A class which mixes verbose test case functionality with the built-in Django Rest Framework APITestCase class.
    """
