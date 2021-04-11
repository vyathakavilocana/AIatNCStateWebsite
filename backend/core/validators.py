from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from jsonschema import validate
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError


class JSONSchemaValidator(BaseValidator):
    """
    TODO Docs
    https://stackoverflow.com/questions/37642742/django-postgresql-json-field-schema-validation
    """

    def compare(self, value, schema):
        """
        TODO Docs
        """
        try:
            validate(value, schema)
        except JSONSchemaValidationError:
            raise DjangoValidationError('%(value)s failed JSON schema check', params={'value': value})
