"""This module contains Django Rest Framework viewsets for events application models."""
from rest_framework import viewsets

from apps.events.serializers import EventSerializer
from apps.events.models import Event


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for Event objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.

        queryset: A queryset of all the Event objects in the database.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
