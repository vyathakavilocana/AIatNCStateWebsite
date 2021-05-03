"""This module contains Django Rest Framework serializers for projects application models."""
from rest_framework import serializers

from apps.projects.models import Project


# noinspection PyMethodMayBeStatic
class ProjectSerializer(serializers.ModelSerializer):
    """A simple Django Rest Framework serializer for the Project model.

    The serialized representation of a project object includes its name, list of authors, long-form description, the
    relative URL of its ``image`` field, the URL to an external website where the project is hosted, the label
    associated with the object's ``status`` field, and an object containing a formatted representation of the date and
    time of its ``modified``.

    Attributes:  # noqa
        image_url: A serializer method field that is included in the serialized representation of a Project object
        rather than the object's ``image`` field itself.
        status: A serializer method field which retrieves and returns the label associated with the Project object's
        ``status``.
        modified: A serializer method field which retrieves and returns formatted representations of the date and time
        when the project was last modified in a dictionary.
    """
    image_url = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    modified = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        """A get method for the ProjectSerializer class' ``image_url`` attribute.

        Args:
            obj: The instance of the Project model class that is being serialized.

        Returns:
            The relative URL where the project's image can be requested from, or an empty string of the project does not
            have an associated image file.
        """
        if obj.image:
            return obj.image.url

        return ''

    def get_status(self, obj):
        """A get method for the ProjectSerializer class' ``status`` attribute.

        Args:
            obj: The Project object that is being serialized.

        Returns:
            The verbose label associated with the ``status`` of the Project object.
        """
        return Project.ProjectStatus(obj.status).label

    def get_modified(self, obj):
        """A get method for the ProjectSerializer class' ``modified`` attribute.

        Args:
            obj: The Project object that is being serialized.

        Returns:
            A dictionary that contains 'date' and 'time' properties containing formatted string representations of the
            date and time when the project was last edited.
        """
        return {
            'date': obj.modified.strftime('%m-%d-%Y'),
            'time': obj.modified.strftime('%I:%M %p'),
        }

    class Meta:
        """A class which defines basic configuration options for the ProjectSerializer class.

        Attributes:  # noqa
            model: The model class that the ProjectSerializer class serializes.

            fields: A list of the fields to include in the serialized representation of a Project model instance.
        """
        model = Project
        fields = ['name', 'authors', 'description', 'image_url', 'url', 'status', 'modified']
