"""This module contains Django Rest Framework viewsets for events application models."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.events.serializers import EventSerializer
from apps.events.models import Event


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for Event objects.

    TODO Update docs

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.

        queryset: A queryset of all the Event objects in the database.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all().prefetch_related('contacts')

    @action(detail=False)
    def upcoming(self, request):
        """TODO Docs
        """
        qs = [e for e in self.queryset if e.upcoming]

        if 'count' in request.query_params:
            try:
                serializer = self.get_serializer(qs[:int(request.query_params['count'])], many=True)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)
