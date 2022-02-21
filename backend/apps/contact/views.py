"""This module contains Django Rest Framework viewsets for contact application models."""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.contact.models import (
    GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm
)
from apps.contact.serializers import (
    GuestSpeakerContactFormSerializer, MentorContactFormSerializer, EventOrganizerContactFormSerializer,
    PartnerContactFormSerializer
)


class ContactFormViewSetBase(viewsets.ModelViewSet):
    """A base viewset which acts as a create-only API endpoint for ContactForm objects.
    """
    def get_permissions(self):
        """Dynamically determines the permission classes for the view set based on the action being performed. Only
        admin users are permitted to carry out any action other than `create`. All `create` requests are permitted.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class GuestSpeakerContactFormViewSet(ContactFormViewSetBase):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for GuestSpeakerContactForm objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.
        queryset: The set of objects used to populate responses.
    """
    serializer_class = GuestSpeakerContactFormSerializer
    queryset = GuestSpeakerContactForm.objects.all()


class MentorContactFormViewSet(ContactFormViewSetBase):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for MentorContactForm objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.
        queryset: The set of objects used to populate responses.
    """
    serializer_class = MentorContactFormSerializer
    queryset = MentorContactForm.objects.all()


class EventOrganizerContactFormViewSet(ContactFormViewSetBase):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for EventOrganizerContactForm objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.
        queryset: The set of objects used to populate responses.
    """
    serializer_class = EventOrganizerContactFormSerializer
    queryset = EventOrganizerContactForm.objects.all()


class PartnerContactFormViewSet(ContactFormViewSetBase):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for PartnerContactForm objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.
        queryset: The set of objects used to populate responses.
    """
    serializer_class = PartnerContactFormSerializer
    queryset = PartnerContactForm.objects.all()
