"""This module contains Django Rest Framework serializers for announcement application models."""
from rest_framework import serializers

from apps.announcements.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """A simple Django Rest Framework serializer for the Announcement model.

    The serialized representation of an announcement object includes its title, body content represented with JSON, and
    an object containing a formatted representation of the date and time of its ``created`` field.

    Attributes:  # noqa
        created: A serializer method field which retrieves and returns formatted representations of the date and time
        when the announcement was created in a dictionary.
    """
    created = serializers.SerializerMethodField(read_only=True)

    # noinspection PyMethodMayBeStatic
    def get_created(self, obj):
        """A get method for the AnnouncementSerializer class' ``created`` attribute.

        Args:
            obj: The Announcement object that is being serialized.

        Returns:
            A dictionary that contains 'date' and 'time' properties containing a formatted string representations of the
            date and time when the announcement was created.
        """
        return {
            'date': obj.created.strftime('%m-%d-%Y'),
            'time': obj.created.strftime('%I:%M %p'),
        }

    class Meta:
        """A class which defines basic configuration options for the AnnouncementSerializer class.

        Attributes:  # noqa
            model: The model class that the AnnouncementSerializer class serializes.

            fields: A list of the fields to include in the serialized representation of an Announcement model instance.
        """
        model = Announcement
        fields = ['title', 'body', 'created']
