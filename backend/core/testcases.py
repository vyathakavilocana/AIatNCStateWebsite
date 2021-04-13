"""TODO Docs"""
from django.test import TestCase


class VerboseTestCase(TestCase):
    """TODO Docs
    """
    @classmethod
    def setUpClass(cls):
        """TODO Docs
        """
        super().setUpClass()
        if hasattr(cls, 'message'):
            print('\n' + getattr(cls, 'message'))
