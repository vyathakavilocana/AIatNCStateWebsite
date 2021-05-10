"""TODO Docs"""
from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from apps.contact.models import (
    ContactFormBase, GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm
)


class ContactFormBaseChildAdmin(PolymorphicChildModelAdmin):
    """TODO Docs
    """
    base_model = ContactFormBase

    # TODO ?
    """
    base_form = ...
    base_fieldsets = (
        ...
    )
    """


@admin.register(GuestSpeakerContactForm)
class GuestSpeakerContactFormAdmin(ContactFormBaseChildAdmin):
    """TODO Docs
    """
    base_model = GuestSpeakerContactForm


@admin.register(MentorContactForm)
class MentorContactFormFormAdmin(ContactFormBaseChildAdmin):
    """TODO Docs
    """
    base_model = MentorContactForm


@admin.register(EventOrganizerContactForm)
class EventOrganizerContactFormAdmin(ContactFormBaseChildAdmin):
    """TODO Docs
    """
    base_model = EventOrganizerContactForm


@admin.register(PartnerContactForm)
class PartnerContactFormAdmin(ContactFormBaseChildAdmin):
    """TODO Docs
    """
    base_model = PartnerContactForm


@admin.register(ContactFormBase)
class ContactFormBaseParentAdmin(PolymorphicParentModelAdmin):
    """TODO Docs
    """
    base_model = ContactFormBase
    child_models = (GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm)
    list_filter = (PolymorphicChildModelFilter,)
