"""This module contains Django Rest Framework serializers for contact application models."""
from rest_framework import serializers

from core.models import ContactInfo
from core.serializers import ContactInfoSerializer
from apps.contact.models import (
    GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm
)


class ContactFormSerializerBase(serializers.ModelSerializer):
    """A Django Rest Framework serializer for models which inherit from the ContactFormBase model.

    Attributes:  # noqa
        contacts: A nested serializer for the ContactForm object's related ContactInfo objects. When a ContactInfo
        object is serialized, related ContactInfo objects are serialized and included in the serialized representation
        of the ContactForm object.
    """
    contacts = ContactInfoSerializer(many=True, read_only=False)

    def create(self, validated_data):
        """Conditionally constructs the appropriate form type with validated request data based on subclass name when a
        new ContactForm object is being created. Additionally, this method handles the creation of related ContactInfo
        objects after creating the form object.

        Args:
            validated_data: the validated request data to construct a new form object with
        """
        contacts = validated_data.pop('contacts', None)

        if self.__class__.__name__ == 'GuestSpeakerContactFormSerializer':
            form = GuestSpeakerContactForm(**validated_data)
        elif self.__class__.__name__ == 'MentorContactFormSerializer':
            form = MentorContactForm(**validated_data)
        elif self.__class__.__name__ == 'EventOrganizerContactFormSerializer':
            form = EventOrganizerContactForm(**validated_data)
        elif self.__class__.__name__ == 'PartnerContactFormSerializer':
            form = PartnerContactForm(**validated_data)
        else:
            from rest_framework.exceptions import APIException
            raise APIException('Unsupported contact form type.', 400)

        form.save()
        for contact_data in contacts:
            contact = ContactInfo(**contact_data, content_object=form)
            contact.save()

        return form

    class Meta:
        """A class which defines configuration options for the ContactFormSerializerBase class.

        Attributes:  # noqa
            fields: A list of the fields to include in the serialized representation of a ContactForm model instance.
        """
        fields = [
            'first_name', 'last_name', 'affiliation', 'contacts', 'thoughts',
        ]


class GuestSpeakerContactFormSerializer(ContactFormSerializerBase):
    """A Django Rest Framework serializer for the GuestSpeakerContactForm model.
    """
    class Meta:
        """A class which defines configuration options for the GuestSpeakerContactFormSerializer class.

        Attributes:  # noqa
            model: The model that the GuestSpeakerContactFormSerializer class serializes.
            fields: A list of the fields to include in the serialized representation of a GuestSpeakerContactForm model
            instance.
        """
        model = GuestSpeakerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'topic', 'availability', 'length', 'visual_aids', 'addl_visual_aids', 'addl_tech', 'consent_audio_rec',
            'consent_video_rec', 'consent_streaming', 'consent_materials',
        ]


class MentorContactFormSerializer(ContactFormSerializerBase):
    """A Django Rest Framework serializer for the MentorContactForm model.
    """
    class Meta:
        """A class which defines configuration options for the MentorContactFormSerializer class.

        Attributes:  # noqa
            model: The model that the MentorContactFormSerializer class serializes.
            fields: A list of the fields to include in the serialized representation of a MentorContactForm model
            instance.
        """
        model = MentorContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'students', 'field_type', 'field_name', 'field_description', 'availability_start', 'availability_end',
            'meeting_information', 'weekly_minutes',
        ]


class EventOrganizerContactFormSerializer(ContactFormSerializerBase):
    """A Django Rest Framework serializer for the EventOrganizerContactForm model.
    """
    class Meta:
        """A class which defines configuration options for the EventOrganizerContactFormSerializer class.

        Attributes:  # noqa
            model: The model that the EventOrganizerContactFormSerializer class serializes.
            fields: A list of the fields to include in the serialized representation of an EventOrganizerContactForm
            model instance.
        """
        model = EventOrganizerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'event_type', 'financial_assistance', 'min_attendees', 'max_attendees', 'advertising'
        ]


class PartnerContactFormSerializer(ContactFormSerializerBase):
    """A Django Rest Framework serializer for the PartnerContactForm model.
    """
    class Meta:
        """A class which defines configuration options for the PartnerContactFormSerializer class.

        Attributes:  # noqa
            model: The model that the PartnerContactFormSerializer class serializes.
            fields: A list of the fields to include in the serialized representation of an PartnerContactForm model
            instance.
        """
        model = PartnerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'commercial', 'industry', 'min_org_size', 'max_org_size', 'funding', 'initiatives'
        ]
