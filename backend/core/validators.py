"""This module contains custom Django validators for cleaning model fields."""
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from jsonschema import validate
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError


class JSONSchemaValidator(BaseValidator):
    """A generic validator for JSONFields which are required to follow a pre-defined JSON schema.

    For example, if you have defined a valid JSON schema named ``MY_JSON_SCHEMA``, and you have a model with a JSONField
    that you would like to adhere to that schema, set the ``validators`` option for the field as follows:

    ``validators=[JSONSchemaValidator(limit_value=MY_JSON_SCHEMA)]``

    Then, the fields of an instance of your model are cleaned, the ``compare(self, value, schema)`` method below will
    attempt to validate the value of the JSONField against the provided schema. See https://json-schema.org/ for more
    information regarding JSON schemas in general.

    Note: This implementation was adapted from the following StackOverflow answer: https://stackoverflow.com/a/49036841
    """

    def compare(self, value, schema):
        """The method which compares the current value of a JSONField with the provided JSON schema for validation.

        First, an attempt is made to validate the specified value against the provided JSON schema. If this operation
        succeeds, the value was successfully validated, so no additional work is needed. Otherwise, the value was not
        successfully validated and a ValidationError is raised by the jsonschema.validate() method. Although the error
        has the same name as the built-in Django ValidationError, simply allowing it to propagate to the caller of this
        can cause issues, such as 500 errors, in the frontend, so the jsonschema ValidationError is caught and a Django
        ValidationError is raised instead.

        Args:
            value: The value to validate.
            schema: The JSON schema to validate the specified value against.

        Raises:
            ValidationError: The value does not follow the provided JSON schema.
        """
        try:
            validate(value, schema)
        except JSONSchemaValidationError:
            raise DjangoValidationError(_('%(value)s failed JSON schema check'), params={'value': value})


def validate_phone(value):
    """TODO Docs

    Args:
        value:
    """
    # TODO Scrub +1 from `value`

    v = ''.join([c for c in value if c.isdigit()])

    if len(v) != 10:
        raise DjangoValidationError(_('%(value)s is not a valid phone number'), params={'value': value})
