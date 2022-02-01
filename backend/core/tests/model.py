"""TODO Docs"""
from django.test import tag
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from core.models import ContactInfo
from core.testcases import VerboseTestCase, Tags
from apps.events.models import Event


class TestContactInfoModel(VerboseTestCase):
    """A Django test case class which contains unit tests for ContactInfo model functionality.

    TODO Update docs
    TODO Unit test for Validation to ensure that ContactInfo objects can only be related to supported object types
     (i.e., Event, or any of the contact form models)

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing ContactInfo model...'

    @classmethod
    def setUpTestData(cls):
        """Creates and saves a valid Event object for creating ContactInfo objects in individual tests.
        """
        cls.event = Event(
            type=Event.EventType.OTHER,
            topics=['Topic 1'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )
        cls.event.save()

    @tag(Tags.MODEL)
    def test_clean_email_type_valid_email(self):
        """Ensure that a ValidationError is not raised for an object with type `EMAIL` and a valid email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            content_object=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_email_type_invalid_email(self):
        """Ensure that a ValidationError is raised for an object with type `EMAIL` and an invalid email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='invalid.email',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_email_type_empty_value(self):
        """Ensure that a ValidationError is raised for an object with type `EMAIL` and an invalid (empty) email value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_phone_type_valid_phone(self):
        """Ensure that a ValidationError is not raised for an object with type `PHONE` and a valid phone number value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.PHONE,
            preferred=False,
            value='(123)-456-7890',
            content_object=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_phone_type_invalid_phone_too_short(self):
        """Ensure that a ValidationError is raised for an object with type `PHONE` and an invalid phone number value.

        Tests a value that is invalid because it contains too few digits.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.PHONE,
            preferred=False,
            value='(123)-456-789',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_phone_type_invalid_phone_too_long(self):
        """Ensure that a ValidationError is raised for an object with type `PHONE` and an invalid phone number value.

        Tests a value that is invalid because it contains too many digits.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.PHONE,
            preferred=False,
            value='(123)-456-78901',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_phone_type_empty_value(self):
        """Ensure that a ValidationError is raised for an object with type `PHONE` and an empty value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.PHONE,
            preferred=False,
            value='',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_other_type_valid_email(self):
        """Ensure that a ValidationError is not raised for an object with type `OTHER` and a valid email value.

        Additionally, ensure that the object's type was properly coerced to `EMAIL`, since its value was a valid email
        address.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value='valid@email.com',
            content_object=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)
        contact.save()
        self.assertEqual(ContactInfo.InfoType.EMAIL, contact.type)

    @tag(Tags.MODEL)
    def test_clean_other_type_valid_phone(self):
        """Ensure that a ValidationError is not raised for an object with type `OTHER` and a valid phone number value.

        Additionally, ensure that the object's type was properly coerced to `PHONE`, since its value was a valid phone
        number.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value='(123)-456-7890',
            content_object=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)
        contact.save()
        self.assertEqual(ContactInfo.InfoType.PHONE, contact.type)

    @tag(Tags.MODEL)
    def test_clean_other_type_valid_value(self):
        """Ensure that a ValidationError is not raised for an object with type `OTHER` and a valid "other" value.

        A valid "other" value is any string that is not empty and that does not only contain whitespace.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value='Some arbitrary contact information',
            content_object=self.event
        )
        contact.save()

        self.assertNotRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_other_type_empty_value_(self):
        """Ensure that a ValidationError is raised for an object with type `OTHER` and an empty value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value='',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_other_type_invalid_value(self):
        """Ensure that a ValidationError is raised for an object with type `OTHER` and an invalid value.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.OTHER,
            preferred=False,
            value=' \t\n  \r',
            content_object=self.event
        )
        contact.save()

        self.assertRaises(ValidationError, contact.full_clean)

    @tag(Tags.MODEL)
    def test_clean_invalid_relation(self):
        """Ensure that a ValidationError is raised for an object whose `content_object` is not one of the supported
        relation types.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            content_object=self.event
        )
        contact.save()

        test = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            content_object=contact
        )

        self.assertRaises(ValidationError, test.full_clean)

    @tag(Tags.MODEL)
    def test_str(self):
        """Ensure that a ContactInfo object's string representation is an empty string.
        """
        contact = ContactInfo(
            type=ContactInfo.InfoType.EMAIL,
            preferred=False,
            value='valid@email.com',
            content_object=self.event
        )

        self.assertEqual('', str(contact))
