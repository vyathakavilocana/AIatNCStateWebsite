"""This module contains unit tests for backend core validators."""
from django.core.exceptions import ValidationError
from django.test import tag
from jsonschema.exceptions import SchemaError

from core.testcases import VerboseTestCase, Tags
from core.validators import JSONSchemaValidator, validate_phone


class TestJSONSchemaValidator(VerboseTestCase):
    """A test case class which contains unit tests for the JSONSchemaValidator.
    """
    message = 'Testing JSONSchemaValidator class...'

    @classmethod
    def setUpTestData(cls):
        """Set up valid and invalid schemas for the test case once when the test case class is being prepared to run.

        Additionally, initialize a JSONSchemaValidator object for use in the individual unit tests.
        """
        cls.valid_schema = {
            'schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'string',
            'minLength': 1
        }
        cls.invalid_schema = {
            'schema': 'http://json-schema.org/draft-07/schema#',
            'type': 'string',
            'minLength': -1
        }
        cls.validator = JSONSchemaValidator(cls.valid_schema)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_compare_valid_value(self):
        """Ensure that a ValidationError is not raised by `compare()` when passed a valid value and schema.
        """
        self.assertNotRaises(ValidationError, self.validator.compare, 'Valid string', self.valid_schema)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_compare_invalid_value(self):
        """Ensure that a ValidationError is raised by `compare()` when passed an invalid value and valid schema.
        """
        self.assertRaises(ValidationError, self.validator.compare, '', self.valid_schema)

    @tag(Tags.JSON, Tags.VALIDATION)
    def test_compare_invalid_schema(self):
        """Ensure that a SchemaError is raised by `compare()` when passed a valid value and invalid schema.
        """
        self.assertRaises(SchemaError, self.validator.compare, 'Valid string', self.invalid_schema)


class TestPhoneValidator(VerboseTestCase):
    """A test case class which contains unit tests for phone number validation.
    """
    message = 'Testing validate_phone method...'

    @tag(Tags.VALIDATION)
    def test_validate_valid_phone(self):
        """Ensure that a ValidationError is not raised when validating a valid phone number.

        The valid phone number in this case does not include the U.S. country code.
        """
        self.assertNotRaises(ValidationError, validate_phone, '123-456-7890')

    @tag(Tags.VALIDATION)
    def test_validate_valid_phone_country_code(self):
        """Ensure that a ValidationError is not raised when validating a valid phone number.

        The valid phone number in this case includes the U.S. country code.
        """
        self.assertNotRaises(ValidationError, validate_phone, '+1 (123)-456-7890')

    @tag(Tags.VALIDATION)
    def test_validate_invalid_phone_too_long(self):
        """Ensure that a ValidationError is raised when validating an invalid phone number.

        The invalid phone number in this case includes the U.S. country code without a '+' before it, so it appears
        to have too many digits.
        """
        self.assertRaises(ValidationError, validate_phone, '1 (123)-456-7890')

    @tag(Tags.VALIDATION)
    def test_validate_invalid_phone_too_short(self):
        """Ensure that a ValidationError is raised when validating an invalid phone number with too few digits.
        """
        self.assertRaises(ValidationError, validate_phone, '(123)-456-789')
