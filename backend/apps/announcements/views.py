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
        """Overrides the default ModelViewSet list action to check for query parameters.

        The only supported query parameter is `count` which may be used to specify the exact number of announcements to
        include in the response. Note: If the specified number of announcements to include in the response exceeds the
        number of announcements in the database, all of the announcements are included in the response rather than
        raising an error or returning an HTTP 400 response.
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

