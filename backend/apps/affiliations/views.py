"""This module contains Django Rest Framework viewsets for affiliations application models."""
from rest_framework import viewsets

from apps.affiliations.serializers import AffiliateSerializer
from apps.affiliations.models import Affiliate


class AffiliateViewSet(viewsets.ModelViewSet):
    """A simple Django Rest Framework viewset, which acts as an API endpoint for the Affiliate model.

    Attributes:  # noqa
        serializer_class: The ModelSerializer class that serializes objects in the class' ``queryset`` attribute for
        retrieval via the API endpoint.

        queryset: A queryset containing all of the objects that can be accessed from the
    """
    serializer_class = AffiliateSerializer
    queryset = Affiliate.objects.all()
