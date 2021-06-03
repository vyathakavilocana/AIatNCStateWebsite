"""This module contains Django models that are not primarily used in only one Django application."""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

from core.validators import validate_phone


class ContactInfo(models.Model):
    """A Django database model which represents a point of contact for a club event.

    In the PostgreSQL database, information for a method of contact has a type (email/phone/other), a field representing
    whether or not the method of contact is preferred, the actual value of the method of contact, and a many-to-one,
    generic relationship to various other models (namely the Event and various ContactForm* models).

    Attributes:  # noqa
        type: A CharField containing the type of contact form. The available types are defined in the InfoType class.

        preferred: A BooleanField representing whether or not the contact method is a preferred method of contact.

        value: A CharField containing the actual value of the method of contact, whether that is a phone number, email
        address, or otherwise.

        content_type: Defines a many-to-one relationship from ContactInfo objects to the ContentType of the related
        ``content_object``.

        object_id: The primary key of the ``content_object`` for its ContentType.

        content_object: A generic many-to-one relationship which relates a ContactInfo object to an object whose type is
        is found with the ``content_type`` foreign key and whose own foreign key is stored in ``object_id``.
    """

    class InfoType(models.TextChoices):
        """Defines the supported types of contact information for the ContactInfo model's ``type`` field.

        Attributes:  # noqa
            EMAIL: A 2 character identifier and lazily-evaluated label representing the choice of an email address.

            PHONE: A 2 character identifier and lazily-evaluated label representing the choice of a phone number.

            OTHER: A 2 character identifier and lazily-evaluated label representing the catch-all choice for all other
            forms of contact.
        """
        EMAIL = 'EM', _('Email Address')
        PHONE = 'PH', _('Phone Number')
        OTHER = 'OT', _('Other Form of Contact')

    _SUPPORTED_RELATION_TYPES = (
        'Event', 'GuestSpeakerContactForm', 'MentorContactForm', 'EventOrganizerContactForm', 'PartnerContactForm',
    )

    type = models.CharField(
        max_length=2,
        choices=InfoType.choices,
        default=InfoType.EMAIL,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Contact Information Type',
    )
    preferred = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        editable=True,
        unique=False,
        verbose_name='Preferred Method of Contact',
    )
    value = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='',
        editable=True,
        unique=False,
        verbose_name='Contact Value',
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        editable=True,
        related_name='contacts',
        related_query_name='contacts',
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        """This method defines custom ContactInfo model validation logic.

        First, the type of the related ``content_object``
        Then, it validates a model instance's ``value`` field based upon its ``type`` (e.g., ``value`` is validated as
        a phone number if the instance's ``type`` is ``InfoType.PHONE``). Finally, it attempts to coerce the value in a
        model instance's ``type`` field to the appropriate type based on its ``value`` field. That is, if a model
        instance's ``type`` field contains ``InfoType.OTHER``, but its ``value`` field contains a valid email address,
        the method will automatically set the instance's ``type`` field to ``InfoType.EMAIL``.
        """
        if not any(self.content_object.__class__.__name__ == t for t in self._SUPPORTED_RELATION_TYPES):
            raise ValidationError(
                f'Unsupported ContentType "{type(self.content_object.__class__.__name__)}" supplied for '
                + 'GenericForeignKey relation.'
            )

        if self.type == self.InfoType.EMAIL:
            validate_email(self.value)
            return
        elif self.type == self.InfoType.PHONE:
            validate_phone(self.value)
            return

        # Attempt to coerce the type to `EMAIL` if it is currently `OTHER` but its value is a valid email.
        try:
            validate_email(self.value)
            self.type = self.InfoType.EMAIL
            return
        except ValidationError:
            pass

        # Attempt to coerce the type to `EMAIL` if it is currently `OTHER` but its value is a valid email.
        try:
            validate_phone(self.value)
            self.type = self.InfoType.PHONE
            return
        except ValidationError:
            pass

        if len(self.value.strip()) == 0:
            raise ValidationError('Contact value must not only contain whitespace')

    def __str__(self):
        """Defines the string representation of a ContactInfo object to be an empty string.
        """
        return ''

    class Meta:
        """This class contains meta-options for the ContactInfo model.

        Attributes:  # noqa
            ordering: Specifies that ContactInfo objects should be in descending order by whether they are preferred or
            not (i.e., preferred ContactInfo objects first, and non-preferred ContactInfo objects last).
        """
        ordering = ['-preferred']
