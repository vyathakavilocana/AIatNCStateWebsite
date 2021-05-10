from rest_framework import serializers

from core.models import ContactInfo


class ContactInfoSerializer(serializers.ModelSerializer):
    """A Django Rest Framework serializer for the ContactInfo model.

    TODO Update docs

    The serialized representation of a ContactInfo model instance includes the label associated with the instance's
    ``type`` field as well as its ``preferred`` and ``value`` fields.

    Attributes:  # noqa
        type: A serializer method field which retrieves and returns the label associated with the ContactInfo object's
        ``type``.
    """
    type = serializers.SerializerMethodField(read_only=True)

    # noinspection PyMethodMayBeStatic
    def get_type(self, obj):
        """A get method for the AffiliateSerializer class' ``type`` attribute.

        Args:
            obj: The instance of the ContactInfo model class that is being serialized.

        Returns:
            The verbose label associated with the ``type`` of the ContactInfo object.
        """
        return ContactInfo.InfoType(obj.type).label

    class Meta:
        """A class which defines configuration options for the ContactInfoSerializer class.

        Attributes:  # noqa
            model: The model that the ContactInfoSerializer class serializes.

            fields: A list of the fields to include in the serialized representation of a ContactInfo model instance.
        """
        model = ContactInfo
        fields = ['type', 'preferred', 'value']
