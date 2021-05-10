"""This module contains Django Rest Framework viewsets for announcements application models."""
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.announcements.serializers import AnnouncementSerializer
from apps.announcements.models import Announcement


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for Announcement objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.

        queryset: A queryset of all the Announcement objects in the database.
    """
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def list(self, request, **kwargs):
        """TODO Docs
        """
        if 'count' in request.query_params:
            try:
                serializer = self.get_serializer(self.queryset[:int(request.query_params['count'])], many=True)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(self.queryset, many=True)

        return Response(serializer.data)

