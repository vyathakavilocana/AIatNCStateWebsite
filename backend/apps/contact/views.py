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
    """TODO Docs
    """
    def get_permissions(self):
        """TODO Docs
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class GuestSpeakerContactFormViewSet(ContactFormViewSetBase):
    """TODO Docs
    """
    serializer_class = GuestSpeakerContactFormSerializer
    queryset = GuestSpeakerContactForm.objects.all()


class MentorContactFormViewSet(ContactFormViewSetBase):
    """TODO Docs
    """
    serializer_class = MentorContactFormSerializer
    queryset = MentorContactForm.objects.all()


class EventOrganizerContactFormViewSet(ContactFormViewSetBase):
    """TODO Docs
    """
    serializer_class = EventOrganizerContactFormSerializer
    queryset = EventOrganizerContactForm.objects.all()


class PartnerContactFormViewSet(ContactFormViewSetBase):
    """TODO Docs
    """
    serializer_class = PartnerContactFormSerializer
    queryset = PartnerContactForm.objects.all()
