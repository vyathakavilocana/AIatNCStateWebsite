"""This module contains Django Rest Framework serializers for events application models."""
from rest_framework import serializers

from core.serializers import ContactInfoSerializer
from apps.events.models import Event


# noinspection PyMethodMayBeStatic
class EventSerializer(serializers.ModelSerializer):
    """A Django Rest Framework serializer for the ContactInfo model.

    TODO Update all docs

    The serialized representation of an Event model instance includes the label associated with the instance's ``type``
    field, objects containing formatted representations of the date and time of its ``start`` and ``end`` fields, a
    nested serializer for associated ContactInfo objects, as well as its ``topics``, ``calendar_link`` and
    ``meeting_link`` fields.

    Attributes:  # noqa
        type: A serializer method field which retrieves and returns the label associated with the Event object's
        ``type``.

        start: A serializer method field which retrieves and returns formatted representations of the date and time when
        the event starts in a dictionary.

        end: A serializer method field which retrieves and returns formatted representations of the date and time when
        the event ends in a dictionary.

        contact: A nested serializer for the Event object's related ContactInfo objects. When an Event object is
        serialized, related ContactInfo objects are serialized and included in the serialized representation of the
        Event object.
    """
    type = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    contacts = ContactInfoSerializer(many=True, read_only=True)

    def get_type(self, obj):
        """A get method for the EventSerializer class' ``type`` attribute.

        Args:
            obj: The Event object that is being serialized.

        Returns:
            The verbose label associated with the ``type`` of the Event object.
        """
        return Event.EventType(obj.type).label

    def get_start(self, obj):
        """A get method for the EventSerializer class' ``start`` attribute.

        Args:
            obj: The Event object that is being serialized.

        Returns:
            A dictionary that contains 'date' and 'time' properties containing formatted string representations of the
            Event object's start date and time.
        """
        return {
            'date': obj.start.strftime('%m-%d-%Y'),
            'time': obj.start.strftime('%I:%M %p'),
        }

    def get_end(self, obj):
        """A get method for the EventSerializer class' ``end`` attribute.

        Args:
            obj: The Event object that is being serialized.

        Returns:
            A dictionary that contains 'date' and 'time' properties containing formatted string representations of the
            Event object's end date and time.
        """
        return {
            'date': obj.end.strftime('%m-%d-%Y'),
            'time': obj.end.strftime('%I:%M %p'),
        }

    class Meta:
        """A class which defines configuration options for the EventSerializer class.

        Attributes:  # noqa
            model: The model that the EventSerializer class serializes.

            fields: A list of the fields to include in the serialized representation of an Event model instance.
        """
        model = Event
        fields = ['type', 'topics', 'start', 'end', 'calendar_link', 'meeting_link', 'contacts', 'upcoming']
