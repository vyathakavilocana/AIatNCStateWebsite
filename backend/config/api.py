from rest_framework import routers
from apps.users.views import UserViewSet
from apps.affiliations.views import AffiliateViewSet
from apps.events.views import EventViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)
api.register(r'affiliates', AffiliateViewSet)
api.register(r'events', EventViewSet)
