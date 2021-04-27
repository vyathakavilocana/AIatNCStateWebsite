"""This module contains Django Rest Framework serializers for affiliations application models."""
from rest_framework import serializers

from apps.affiliations.models import Affiliate


class AffiliateSerializer(serializers.ModelSerializer):
    """A simple Django Rest Framework serializer for the Affiliate model.

    The serialized representation of an affiliate model instance includes the instance's ``name`` and ``website``
    attributes, as well as the relative URL from which the affiliate's logo can be requested.

    Attributes:  # noqa
        logo_url: A serializer method field that is included in the serialized representation of an Affiliate model
        instance rather than the instance's ``logo`` attribute itself.
    """
    logo_url = serializers.SerializerMethodField(read_only=True)

    # noinspection PyMethodMayBeStatic
    def get_logo_url(self, obj):
        """A get method for the AffiliateSerializer class' ``logo_url`` attribute.

        This method defines the logic that is evaluated when serializing an Affiliate model instance and retrieving the
        logo_url attribute. It simply returns the relative URL of the FieldFile instance that is stored in the Affiliate
        class' ``logo`` attribute.

        Args:
            obj: The instance of the Affiliate model class that is being serialized.

        Returns:
            The relative URL where the affiliate's logo can be requested from.
        """
        return obj.logo.url

    class Meta:
        """A class which defines basic configuration options for the AffiliateSerializer class.

        Attributes:  # noqa
            model: The model class that the AffiliateSerializer class serializes.

            fields: A list of the fields to include in the serialized representation of an Affiliate model instance.
        """
        model = Affiliate
        fields = ['name', 'logo_url', 'website']
