"""This module contains unit tests for the contact application's Django models."""
from django.core.exceptions import ValidationError
from django.test import tag

from apps.contact.models import (
    GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm
)
from core.testcases import VerboseTestCase, Tags


class TestContactFormBaseModel(VerboseTestCase):
    """A Django test case class which contains unit tests for ContactFormBase model functionality.
    """
    message = 'Testing ContactFormBase model...'

    @tag(Tags.MODEL)
    def test_str(self):
        """Ensure that the string representation of ContactFormBase objects is correctly implemented.

        Note: Since all other contact form models are subclasses of the ContactFormBase class, and they do not implement
        their own `__str__` methods, any of the contact form models can be used to test this functionality.
        """
        fname = 'John'
        lname = 'Smith'
        form = PartnerContactForm(
            first_name=fname,
            last_name=lname
        )

        form.save()
        self.assertEqual(f'{fname} {lname} - {form.submitted.strftime("%m-%d-%Y")}', str(form))


class TestGuestSpeakerContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for GuestSpeakerContactForm model functionality.
    """
    message = 'Testing GuestSpeakerContactForm model...'

    @classmethod
    def setUpTestData(cls):
        """Set up class attributes to be used to construct GuestSpeakerContactForm objects in individual tests.
        """
        cls.fname = 'John'
        cls.lname = 'Smith'
        cls.topic = 'AI/ML'
        cls.length = 90

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_not_array(self):
        """Ensure that the availability field must be an array.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability={}
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_empty_array(self):
        """Ensure that an empty array is an invalid value for the availability field.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_array_too_long(self):
        """Ensure that an array of length greater than three is an invalid value for the availability field.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_empty_object_in_array(self):
        """Ensure that an empty object in an array is not a valid value for the availability field.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_only_date(self):
        """Ensure that an array containing an object with only a `date` property is an invalid value.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018-11-13'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_only_time(self):
        """Ensure that an array containing an object with only a `time` property is an invalid value.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'time': '20:20:39+00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_addl_prop(self):
        """Ensure that an array containing an object with `date`, `time` and an arbitrary third property is invalid.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018-11-13', 'time': '20:20:39+00:00', 'additional': 'property'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_invalid_date(self):
        """Ensure that an array containing an object with valid `time`, but invalid `date` is invalid.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018abc-09-p14', 'time': '20:20:39+00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_invalid_time(self):
        """Ensure that an array containing an object with valid `date`, but invalid `time` is invalid.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018-11-13', 'time': '20p:p20:3'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_availability_object_with_invalid_date_and_time(self):
        """Ensure that an array containing an object with invalid `date` and `time` is invalid.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018abc-09-p14', 'time': '20p:p20:3'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_(self):
        """Ensure that no ValidationError is raised when saving a valid form object.
        """
        form = GuestSpeakerContactForm(
            first_name=self.fname,
            last_name=self.lname,
            topic=self.topic,
            length=self.length,
            availability=[
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'},
                {'date': '2018-11-13', 'time': '20:20:39+00:00'}
            ]
        )
        self.assertNotRaises(ValidationError, form.full_clean)


class TestMentorContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for MentorContactForm model functionality.
    """
    message = 'Testing MentorContactForm model...'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_students_less_than_one(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_students_greater_than_six(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_one(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_six(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_between_one_and_six(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_not_array(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_empty_array(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_empty_object_in_array(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_only_weekday(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_only_time(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_addl_prop(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_weekday(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_time(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_weekday_and_time(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_meeting_information(self):
        """TODO Docs
        """
        self.not_implemented()


class TestEventOrganizerContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for EventOrganizerContactForm model functionality.
    """
    message = 'Testing EventOrganizerContactForm model...'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_min_attendees_too_small(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_max_attendees_too_small(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_attendees_min_greater_than_max(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_attendees_range(self):
        """TODO Docs
        """
        self.not_implemented()


class TestPartnerContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for PartnerContactForm model functionality.
    """
    message = 'Testing PartnerContactForm model...'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_min_org_size_too_small(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_max_org_size_too_small(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_org_sizes_min_greater_than_max(self):
        """TODO Docs
        """
        self.not_implemented()

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_org_size_range(self):
        """TODO Docs
        """
        self.not_implemented()
