"""This module contains unit tests for the contact application's Django models."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import tag
from django.utils import timezone

from apps.contact.models import (
    GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm, AdminComment
)
from apps.events.models import Event
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
    def test_valid(self):
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

    @classmethod
    def setUpTestData(cls):
        """Set up class attributes to be used to construct GuestSpeakerContactForm objects in individual tests.
        """
        cls.first_name = 'John'
        cls.last_name = 'Smith'
        cls.students = 4
        cls.field_type = 'Industry'
        cls.field_name = 'AI/ML'
        cls.availability_start = timezone.now()
        cls.meeting_information = [{'weekday': 'Monday', 'time': '18:00:00+00:00'}]
        cls.weekly_minutes = 120

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_students_less_than_one(self):
        """Ensure that a ValidationError is raised for an invalid (<1) number of students.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            meeting_information=self.meeting_information,
            weekly_minutes=self.weekly_minutes,
            students=0
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_students_greater_than_six(self):
        """Ensure that a ValidationError is raised for an invalid (>6) number of students.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            meeting_information=self.meeting_information,
            weekly_minutes=self.weekly_minutes,
            students=8
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_one(self):
        """Ensure that a ValidationError is not raised for a valid number of students (1).
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            meeting_information=self.meeting_information,
            weekly_minutes=self.weekly_minutes,
            students=1
        )
        self.assertNotRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_six(self):
        """Ensure that a ValidationError is not raised for a valid number of students (6).
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            meeting_information=self.meeting_information,
            weekly_minutes=self.weekly_minutes,
            students=6
        )
        self.assertNotRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_students_between_one_and_six(self):
        """Ensure that a ValidationError is not raised for a valid number of students (between 1-6).
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            meeting_information=self.meeting_information,
            weekly_minutes=self.weekly_minutes,
            students=5
        )
        self.assertNotRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_not_array(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is not an array.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information={}
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_empty_array(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an empty array.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_empty_object_in_array(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an empty object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[{}]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_only_weekday(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (only has `weekday` property) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Monday'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_only_time(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (only has `time` property) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'time': '18:00:00+00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_object_with_addl_prop(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (has an additional property) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Monday', 'time': '18:00:00+00:00', 'additional': 'property'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_weekday(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (has and invalid `weekday` property) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Fursday', 'time': '18:00:00+00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_time(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (has an invalid `time` property) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Thursday', 'time': '18p:00:T00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_meeting_info_invalid_weekday_and_time(self):
        """Ensure that a ValidationError is raised for an invalid meeting_information value that is an array containing
        an invalid (has invalid `weekday` and `time` properties) object.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Fursday', 'time': '18p:00:T00:00'}
            ]
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_meeting_information(self):
        """Ensure that a ValidationError is not raised for a meeting_information value that is an array containing
        valid objects.
        """
        form = MentorContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            students=self.students,
            field_type=self.field_type,
            field_name=self.field_name,
            availability_start=self.availability_start,
            weekly_minutes=self.weekly_minutes,
            meeting_information=[
                {'weekday': 'Monday', 'time': '14:00:00+00:00'},
                {'weekday': 'Tuesday', 'time': '18:00:00+00:00'},
                {'weekday': 'Wednesday', 'time': '18:00:00+00:00'},
                {'weekday': 'Thursday', 'time': '14:00:00+00:00'},
            ]
        )
        self.assertNotRaises(ValidationError, form.full_clean)


class TestEventOrganizerContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for EventOrganizerContactForm model functionality.
    """
    message = 'Testing EventOrganizerContactForm model...'

    @classmethod
    def setUpTestData(cls):
        """Set up class attributes to be used to construct GuestSpeakerContactForm objects in individual tests.
        """
        cls.first_name = 'John'
        cls.last_name = 'Smith'
        cls.event_type = 'Hackathon'
        cls.advertising = 'Self-advertised'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_min_attendees_too_small(self):
        """Ensure that a ValidationError is raised for an invalid (<1) minimum number of attendees.
        """
        form = EventOrganizerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            event_type=self.event_type,
            advertising=self.advertising,
            min_attendees=0,
            max_attendees=100
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_max_attendees_too_small(self):
        """Ensure that a ValidationError is raised for an invalid (=`min_attendees`) maximum number of attendees.
        """
        form = EventOrganizerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            event_type=self.event_type,
            advertising=self.advertising,
            min_attendees=1,
            max_attendees=1
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_attendees_min_greater_than_max(self):
        """Ensure that a ValidationError is raised for an invalid (>`max_attendees`) minimum number of attendees.
        """
        form = EventOrganizerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            event_type=self.event_type,
            advertising=self.advertising,
            min_attendees=1000,
            max_attendees=100
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_attendees_range(self):
        """Ensure that a ValidationError is not raised for a valid range of attendees (`min_attendees`<`max_attendees`).
        """
        form = EventOrganizerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            event_type=self.event_type,
            advertising=self.advertising,
            min_attendees=50,
            max_attendees=100
        )
        self.assertNotRaises(ValidationError, form.full_clean)


class TestPartnerContactFormModel(VerboseTestCase):
    """A Django test case class which contains unit tests for PartnerContactForm model functionality.
    """
    message = 'Testing PartnerContactForm model...'

    @classmethod
    def setUpTestData(cls):
        """Set up class attributes to be used to construct GuestSpeakerContactForm objects in individual tests.
        """
        cls.first_name = 'John'
        cls.last_name = 'Smith'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_min_org_size_too_small(self):
        """Ensure that a ValidationError is raised for an invalid (<1) minimum organization size.
        """
        form = PartnerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            min_org_size=0
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_max_org_size_too_small(self):
        """Ensure that a ValidationError is raised for an invalid (=`min_attendees`) maximum organization size.
        """
        form = PartnerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            max_org_size=1
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_invalid_org_sizes_min_greater_than_max(self):
        """Ensure that a ValidationError is raised for an invalid (>`max_org_size`) minimum number of attendees.
        """
        form = PartnerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            min_org_size=1000,
            max_org_size=100
        )
        self.assertRaises(ValidationError, form.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_valid_org_size_range(self):
        """Ensure that a ValidationError is not raised for a valid range of organization size
        (`min_org_size`<`max_org_size`).
        """
        form = PartnerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            min_org_size=100,
            max_org_size=1000
        )
        self.assertNotRaises(ValidationError, form.full_clean)


class TestAdminCommentModel(VerboseTestCase):
    """A Django test case class which contains unit tests for AdminComment model functionality.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
    """
    message = 'Testing AdminComment model...'

    @classmethod
    def setUpTestData(cls):
        """Set up class attributes to be used to construct GuestSpeakerContactForm objects in individual tests.
        """
        cls.first_name = 'John'
        cls.last_name = 'Smith'

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_clean_valid_relation(self):
        """Ensure that a ValidationError is not raised for an object whose `form` is one of the supported relation
        types.
        """
        form = PartnerContactForm(
            first_name=self.first_name,
            last_name=self.last_name,
            min_org_size=100,
            max_org_size=1000
        )
        form.save()

        comment = AdminComment(
            first_name='John',
            last_name='Adams',
            comment='Comment text',
            form=form
        )
        self.assertNotRaises(ValidationError, comment.full_clean)

    @tag(Tags.MODEL, Tags.VALIDATION)
    def test_clean_invalid_relation(self):
        """Ensure that a ValidationError is raised for an object whose `form` is not one of the supported relation
        types.
        """
        event = Event(
            type=Event.EventType.WORKSHOP,
            topics=['AI/ML'],
            start=timezone.now(),
            end=timezone.now() + timedelta(days=2)
        )
        event.save()

        comment = AdminComment(
            first_name='John',
            last_name='Adams',
            comment='Comment text',
            form=event
        )
        self.assertRaises(ValidationError, comment.full_clean)
