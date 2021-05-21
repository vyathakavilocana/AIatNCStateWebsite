"""This module contains configuration for the API. Endpoints are registered with a Django Rest Framework router."""
from rest_framework import routers

from apps.users.views import UserViewSet
from apps.affiliations.views import AffiliateViewSet
from apps.events.views import EventViewSet
from apps.projects.views import ProjectViewSet
from apps.announcements.views import AnnouncementViewSet
from apps.contact.views import (
    GuestSpeakerContactFormViewSet, MentorContactFormViewSet, EventOrganizerContactFormViewSet,
    PartnerContactFormViewSet
)


# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Register API endpoints
api.register(r'users', UserViewSet, basename='user')
api.register(r'affiliates', AffiliateViewSet, basename='affiliate')
api.register(r'events', EventViewSet, basename='event')
api.register(r'projects', ProjectViewSet, basename='project')
api.register(r'announcements', AnnouncementViewSet, basename='announcement')
api.register(r'contact/speaker', GuestSpeakerContactFormViewSet, basename='speaker-contact-form')
api.register(r'contact/mentor', MentorContactFormViewSet, basename='mentor-contact-form')
api.register(r'contact/organizer', EventOrganizerContactFormViewSet, basename='organizer-contact-form')
api.register(r'contact/partner', PartnerContactFormViewSet, basename='partner-contact-form')
