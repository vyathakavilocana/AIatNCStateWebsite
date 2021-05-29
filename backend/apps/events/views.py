"""This module contains Django Rest Framework viewsets for events application models."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.events.serializers import EventSerializer
from apps.events.models import Event


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for Event objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        """Conditionally evaluates the queryset used to populate responses depending on the action of a request.
        """
        if self.action == 'upcoming':
            return Event.objects.upcoming().prefetch_related('contacts')
        else:
            return Event.objects.all().prefetch_related('contacts')

    def list(self, request, *args, **kwargs):
        """Overrides the built-in ModelViewSet `list` action to check for supported query parameters.

        As-is, the only supported query parameter is `count` which may be used to specify the exact number of events to
        include in the response. Note: If the specified number of events to include in the response exceeds the number
        of events in the database, all the events are included in the response rather than raising an error or returning
        an HTTP 400 response.
        """
        if 'count' in request.query_params:
            try:
                count = int(request.query_params['count'])
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                if count < 1:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(self.get_queryset()[:count], many=True)
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data)

    @action(detail=False)
    def upcoming(self, request, *args, **kwargs):
        """A custom viewset action which returns a list of upcoming Events.
        """
        return self.list(request, *args, **kwargs)
