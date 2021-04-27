"""TODO Docs"""
from enum import Enum
from typing import Type
from django.test import TestCase
from rest_framework.test import APITestCase


class Tags(Enum):
    JSON = 'jsonschema'
    MODEL = 'model'
    API = 'api'


# noinspection PyUnresolvedReferences
class VerboseTestCaseBase:
    """TODO Docs
    """

    @classmethod
    def setUpClass(cls):
        """TODO Docs
        """
        super().setUpClass()
        if hasattr(cls, 'message'):
            print('\n' + getattr(cls, 'message'))

    def assertStartsWith(self, first: str, second: str, message=None):
        """TODO Docs
        """
        self.assertTrue(first.startswith(second), message)

    def assertEndsWith(self, first: str, second: str, message=None):
        """TODO Docs
        """
        self.assertTrue(first.endswith(second), message)

    def assertNotRaises(self, expected_error: Type, call: callable):
        try:
            call()
        except expected_error as e:
            self.fail(e)


class VerboseTestCase(VerboseTestCaseBase, TestCase):
    """TODO Docs
    """


class VerboseAPITestCase(VerboseTestCaseBase, APITestCase):
    """TODO Docs
    """
