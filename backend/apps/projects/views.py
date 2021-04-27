"""This module contains Django Rest Framework viewsets for projects application models."""
from rest_framework import viewsets

from apps.projects.serializers import ProjectSerializer
from apps.projects.models import Project


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """A Django Rest Framework viewset which acts as a read-only API endpoint for Project objects.

    Attributes:  # noqa
        serializer_class: The ModelSerializer subclass that is used when processing requests.

        queryset: A queryset of all the Project objects in the database.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
