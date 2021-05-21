from rest_framework import serializers

from core.models import ContactInfo
from core.serializers import ContactInfoSerializer
from apps.contact.models import (
    GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm
)


class ContactFormSerializerBase(serializers.ModelSerializer):
    """TODO Docs
    """
    contacts = ContactInfoSerializer(many=True, read_only=False)

    def create(self, validated_data):
        """TODO Docs
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
        """TODO Docs
        """
        fields = [
            'first_name', 'last_name', 'affiliation', 'contacts', 'thoughts',
        ]


class GuestSpeakerContactFormSerializer(ContactFormSerializerBase):
    """TODO Docs
    """

    class Meta:
        """TODO Docs
        """
        model = GuestSpeakerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'topic', 'availability', 'length', 'visual_aids', 'addl_visual_aids', 'addl_tech', 'consent_audio_rec',
            'consent_video_rec', 'consent_streaming', 'consent_materials',
        ]


class MentorContactFormSerializer(ContactFormSerializerBase):
    """TODO Docs
    """

    class Meta:
        """TODO Docs
        """
        model = MentorContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'students', 'field_type', 'field_name', 'field_description', 'availability_start', 'availability_end',
            'meeting_information', 'weekly_minutes',
        ]


class EventOrganizerContactFormSerializer(ContactFormSerializerBase):
    """TODO Docs
    """

    class Meta:
        """TODO Docs
        """
        model = EventOrganizerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'event_type', 'financial_assistance', 'min_attendees', 'max_attendees', 'advertising'
        ]


class PartnerContactFormSerializer(ContactFormSerializerBase):
    """TODO Docs
    """

    class Meta:
        """TODO Docs
        """
        model = PartnerContactForm
        fields = ContactFormSerializerBase.Meta.fields + [
            'commercial', 'industry', 'min_org_size', 'max_org_size', 'funding', 'initiatives'
        ]
