"""This module contains unit tests for the announcement application's Django models."""
from django.core.exceptions import ValidationError
from django.test import tag

from apps.announcements.models import Announcement
from core.testcases import VerboseTestCase, Tags


class TestAnnouncementModel(VerboseTestCase):
    """A Django test case class which contains unit tests for the Announcement model.

    Attributes:  # noqa
        message: A string to print to the console before running the individual tests.
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
        """Ensure that attempting to validate an empty list raises a validation error
        """
        announcement = Announcement(
            title='Title',
            body=[]
        )

        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_body_object_no_props(self):
        """Ensure that attempting to validate a list that contains an object with no properties raises a validation
        error
        """
        announcement = Announcement(
            title='Title',
            body=[{}]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_invalid_body_valid_and_invalid_object(self):
        """Ensure that attempting to validate a list that contains a valid object and invalid object raises a
        validation error
        """
        announcement = Announcement(
            title='Title',
            body=[
                {
                    'element': 'p',
                    'content': 'paragraph content'
                },
                {
                    'element': 'img',
                    'alt': 0,
                    'url': 'https://github.com/vyathakavilocana/AIatNCStateWebsite'
                }
            ]
        )

        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_body_valid_object(self):
        """Ensure that attempting to validate a list that contains a single valid object does not raise a validation
        error
        """
        announcement = Announcement(
            title='Title',
            body=[
                {
                    'element': 'h2',
                    'content': 'The quick fox jumps over the dog.'
                }
            ]
        )

        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_valid_body_valid_objects(self):
        """Ensure that attempting to validate a list that contains multiple valid objects does not raise a validation
        error
        """
        announcement = Announcement(
            title='Title',
            body=[
                {
                    'element': 'hr'
                },
                {
                    'element': 'a',
                    'href': 'https://github.com/vyathakavilocana/AIatNCStateWebsite',
                    'content': 'The quick fox jumps over the dog.'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_hr_with_valid_element_valid(self):
        """Ensure that attempting to validate a list that contains a horizontal rule object that has an 'element'
        property with the value 'hr' and no other properties does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'hr'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_hr_with_valid_element_invalid_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a horizontal rule object that has an 'element'
        property with the value 'hr' and some other arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'hr',
                    'chandelier': 'barnacle'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p_valid_element_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a paragraph object with a valid element property
        value 'p' but no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'p'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p_valid_element_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a paragraph object with a valid element property
        value 'p' and a valid content property value but with another arbitrary property/value pair raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'p',
                    'content': 'AI Club is inviting you to the new workshop held on March 6.',
                    'arbitrary': 'arbitrary property and value'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p_valid_element_len_0_content_invalid(self):
        """Ensure that attempting to validate a list that contains a paragraph object with element property value 'p'
        and a content property value with a length of 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'p',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p_valid_element_whitespace_content_invalid(self):
        """Ensure that attempting to validate a list that contains a paragraph object with element property value 'p'
        and a content property value with only whitespace characters (space, '\t', '\f', '\n') raises a validation
        error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'p',
                    'content': "  \t \f \n"
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_p_valid_element_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a paragraph object with element property value 'p'
        and a content property value with a length greater than 1/not only comprised of whitespace characters is valid
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'p',
                    'content': "AI Club is inviting you to the new workshop held on March 6."
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with element property value 'img'
        and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_valid_alt_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img' and a valid alt property value but no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'alt': 'AI Club at NC State Photo 1'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_valid_url_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img' and a valid url property value but no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'url': 'https://github.com/vyathakavilocana/AIatNCStateWebsite'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_valid_url_valid_alt_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img', a valid alt property value, and a valid url property value but has some other arbitrary
        property with arbitrary value raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'alt': 'AI Club at NC State Photo 1',
                    'url': 'https://github.com/vyathakavilocana/AIatNCStateWebsite',
                    'copacabana': 'Barry Manlow'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_valid_url_0_len_alt_valid_url_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img', an alt property value that is a string of length 0, and a valid url property value raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'alt': '',
                    'url': 'https://github.com/vyathakavilocana/AIatNCStateWebsite'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_whitespace_char_alt_valid_url_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img', an alt property value that is a string consisting of only whitespace characters, and a valid
        url property value raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'alt': ' \t \f \n',
                    'url': 'https://github.com/vyathakavilocana/AIatNCStateWebsite'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_img_valid_element_valid_alt_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an image object with a valid element property
        value of 'img', a valid alt property value, and an invalid url property value raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'img',
                    'alt': 'AI at NC State Photo 1',
                    'url': 'therevin',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h1 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h1'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h2_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h2 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h2'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h3_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h3 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h3'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h4_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h4 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h4'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h5_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h5 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h5'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h6_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h6 and no other properties raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h6'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property h1
        and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h1',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h2_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h2 and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h2',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h3_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h3 and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h3',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h4_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h4 and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h4',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h5_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h5 and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h5',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h6_valid_content_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h6 and a valid content property but with another arbitrary property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h6',
                    'content': 'AI at NC State Upcoming Event',
                    'arbitrary': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h1 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h1',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h2_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h2 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h2',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h3_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h3 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h3',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h4_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h4 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h4',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h5_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h5 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h5',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h6_invalid_content_0_len_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h6 and an invalid content property with a string value of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h6',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h1 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h1',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h2_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h2 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h2',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h3_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h3 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h3',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h4_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h4 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h4',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h5 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h5',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h6_invalid_content_whitespace_char_invalid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h6 and an invalid content property with a string value containing only whitespace characters raises a
        validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h6',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h1_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h1 and a valid content property does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h1',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h2_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h2 and a valid content property does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h2',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h3_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h3 and a valid content property does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h3',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h4_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h4 and a valid content property does not raise a validation error
        """

        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h4',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h5_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h5 and a valid content property does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h5',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_h_valid_element_h6_valid_content_valid(self):
        """Ensure that attempting to validate a list that contains a header object with a valid element property
        value h6 and a valid content property does not raise a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'h6',
                    'content': 'AI at NC State Upcoming Event'
                }
            ]
        )
        self.assertNotRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_a_valid_element_no_other_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an anchor object with a valid element property
        value a and no other property raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'a'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_a_valid_element_arbitrary_prop_invalid(self):
        """Ensure that attempting to validate a list that contains an anchor object with a valid element property
        value but an arbitrary property with an arbitrary value raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'a',
                    'arbitraryprop': 'arbitraryvalue'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_a_valid_element_len_0_content_invalid(self):
        """Ensure that attempting to validate a list that contains an anchor object with a valid element property
        value but a content property with a value of a string of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'a',
                    'content': ''
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_a_valid_element_whitespace_char_content_invalid(self):
        """Ensure that attempting to validate a list that contains an anchor object with a valid element property
        value but a content property with a value of a string of length 0 raises a validation error
        """
        announcement = Announcement(
            title="Title",
            body=[
                {
                    'element': 'a',
                    'content': ' \t \f \n'
                }
            ]
        )
        self.assertRaises(ValidationError, announcement.full_clean)
