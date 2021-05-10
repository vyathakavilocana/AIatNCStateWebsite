"""This module contains configuration for the API. Endpoints are registered with a Django Rest Framework router."""
from rest_framework import routers

from apps.users.views import UserViewSet
from apps.affiliations.views import AffiliateViewSet
from apps.events.views import EventViewSet
from apps.projects.views import ProjectViewSet
from apps.announcements.views import AnnouncementViewSet


# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Register API endpoints
api.register(r'users', UserViewSet)
api.register(r'affiliates', AffiliateViewSet)
api.register(r'events', EventViewSet)
api.register(r'projects', ProjectViewSet)
api.register(r'announcements', AnnouncementViewSet)
