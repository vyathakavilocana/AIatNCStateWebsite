"""This module contains contact application configuration for the Django admin site."""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from core.admin import ReadOnlyContactInfoTabularInline, JSONFieldEditorWidget
from apps.contact.models import (
    ContactFormBase, GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm,
    AdminComment
)


class AdminCommentGenericStackedInline(GenericStackedInline):
    """A stacked model inline for the AdminComment model which has a generic relation to all polymorphic child (contact
    form) types. It defines formatting/stylization/layout of the inline, as well as the model fields used to manage the
    generic relationship to a contact form.
    """
    model = AdminComment
    extra = 1
    verbose_name = 'Administrator Comment'
    ct_field = 'form_type'
    ct_fk_field = 'form_id'
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name')
        }),
        (None, {
            'fields': ('comment',)
        })
    )


@admin.register(GuestSpeakerContactForm)
class GuestSpeakerContactFormAdmin(PolymorphicChildModelAdmin):
    """Defines a typical Django model admin page for GuestSpeakerContactForm model instances.
    """
    base_model = GuestSpeakerContactForm
    fieldsets = (
        ('Form Submitter', {
            'fields': (
                ('first_name', 'last_name'),
                'affiliation'
            )
        }),
        ('Form Status', {
            'fields': (
                'submitted',
                ('reviewed', 'ignored')
            )
        }),
        ('Presentation Information', {
            'fields': (
                ('topic', 'length'),
                'availability',
                'visual_aids',
                'addl_visual_aids',
                'addl_tech'
            )
        }),
        ('Consent', {
            'fields': (
                'consent_audio_rec',
                'consent_video_rec',
                'consent_streaming',
                'consent_materials'
            )
        }),
        ('Miscellaneous', {
            'fields': ('thoughts',)
        })
    )
    readonly_fields = (
        'first_name', 'last_name', 'affiliation', 'submitted', 'thoughts', 'reviewed', 'ignored', 'topic',
        'availability', 'length', 'visual_aids', 'addl_visual_aids', 'addl_tech', 'consent_audio_rec',
        'consent_video_rec', 'consent_streaming', 'consent_materials'
    )
    formfield_overrides = {
        models.JSONField: {'widget': JSONFieldEditorWidget}
    }
    inlines = [ReadOnlyContactInfoTabularInline, AdminCommentGenericStackedInline]

    def get_model_perms(self, request):
        """Return an empty dictionary of model permissions. This hides the model from the index sidebar on the site.
        """
        return {}

    def has_delete_permission(self, request, obj=None):
        """Disallows deletion of submitted guest speaker contact forms.
        """
        return False


@admin.register(MentorContactForm)
class MentorContactFormFormAdmin(PolymorphicChildModelAdmin):
    """Defines a typical Django model admin page for MentorContactForm model instances.
    """
    base_model = MentorContactForm
    fieldsets = (
        ('Form Submitter', {
            'fields': (
                ('first_name', 'last_name'),
                'affiliation',
            )
        }),
        ('Form Status', {
            'fields': (
                'submitted',
                ('reviewed', 'ignored')
            )
        }),
        ('Mentor Information', {
            'fields': (
                'field_type',
                'field_name',
                'field_description'
            )
        }),
        ('Mentorship Details', {
            'fields': (
                'students',
                ('availability_start', 'availability_end'),
                'meeting_information',
                'weekly_minutes'
            )
        }),
        ('Miscellaneous', {
            'fields': ('thoughts',)
        })
    )
    readonly_fields = (
        'first_name', 'last_name', 'affiliation', 'submitted', 'thoughts', 'reviewed', 'ignored', 'students',
        'field_type', 'field_name', 'field_description', 'availability_start', 'availability_end',
        'meeting_information', 'weekly_minutes'
    )
    formfield_overrides = {
        models.JSONField: {'widget': JSONFieldEditorWidget}
    }
    inlines = [ReadOnlyContactInfoTabularInline, AdminCommentGenericStackedInline]

    def get_model_perms(self, request):
        """Return an empty dictionary of model permissions. This hides the model from the index sidebar on the site.
        """
        return {}

    def has_delete_permission(self, request, obj=None):
        """Disallows deletion of submitted mentor contact forms.
        """
        return False


@admin.register(EventOrganizerContactForm)
class EventOrganizerContactFormAdmin(PolymorphicChildModelAdmin):
    """Defines a typical Django model admin page for EventOrganizerContactForm model instances.
    """
    base_model = EventOrganizerContactForm
    fieldsets = (
        ('Form Submitter', {
            'fields': (
                ('first_name', 'last_name'),
                'affiliation',
            )
        }),
        ('Form Status', {
            'fields': (
                'submitted',
                ('reviewed', 'ignored')
            )
        }),
        ('Event Information', {
            'fields': (
                'event_type',
                ('min_attendees', 'max_attendees'),
                'advertising',
                'financial_assistance'
            )
        }),
        ('Miscellaneous', {
            'fields': ('thoughts',)
        })
    )
    readonly_fields = (
        'first_name', 'last_name', 'affiliation', 'submitted', 'thoughts', 'reviewed', 'ignored', 'event_type',
        'financial_assistance', 'min_attendees', 'max_attendees', 'advertising'
    )
    formfield_overrides = {
        models.JSONField: {'widget': JSONFieldEditorWidget}
    }
    inlines = [ReadOnlyContactInfoTabularInline, AdminCommentGenericStackedInline]

    def get_model_perms(self, request):
        """Return an empty dictionary of model permissions. This hides the model from the index sidebar on the site.
        """
        return {}

    def has_delete_permission(self, request, obj=None):
        """Disallows deletion of submitted event organizer contact forms.
        """
        return False


@admin.register(PartnerContactForm)
class PartnerContactFormAdmin(PolymorphicChildModelAdmin):
    """Defines a typical Django model admin page for PartnerContactForm model instances.
    """
    base_model = PartnerContactForm
    fieldsets = (
        ('Form Submitter', {
            'fields': (
                ('first_name', 'last_name'),
                'affiliation'
            )
        }),
        ('Form Status', {
            'fields': (
                'submitted',
                ('reviewed', 'ignored')
            )
        }),
        ('Organization Information', {
            'fields': (
                ('commercial', 'industry'),
                ('min_org_size', 'max_org_size')
            )
        }),
        ('Partnership Information', {
            'fields': (
                'funding',
                'initiatives'
            )
        }),
        ('Miscellaneous', {
            'fields': ('thoughts',)
        })
    )
    readonly_fields = (
        'first_name', 'last_name', 'affiliation', 'submitted', 'thoughts', 'reviewed', 'ignored', 'commercial',
        'industry', 'min_org_size', 'max_org_size', 'funding', 'initiatives'
    )
    formfield_overrides = {
        models.JSONField: {'widget': JSONFieldEditorWidget}
    }
    inlines = [ReadOnlyContactInfoTabularInline, AdminCommentGenericStackedInline]

    def get_model_perms(self, request):
        """Return an empty dictionary of model permissions. This hides the model from the index sidebar on the site.
        """
        return {}

    def has_delete_permission(self, request, obj=None):
        """Disallows deletion of submitted partner contact forms.
        """
        return False


class ContactFormTypeFilter(PolymorphicChildModelFilter):
    """A custom filter which allows filtering of submitted contact forms by polymorphic child type (i.e., contact form
    type).
    """
    title = _('Contact Form Type')


@admin.register(ContactFormBase)
class ContactFormBaseParentAdmin(PolymorphicParentModelAdmin):
    """Defines a polymorphic Django model admin page with which contains all types of contact form models, which
    includes filtering capabilities by contact form type and whether forms have been reviewed or ignored.
    """
    base_model = ContactFormBase
    child_models = (GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm)
    list_filter = (ContactFormTypeFilter, 'reviewed', 'ignored')

    def has_add_permission(self, request):
        """Disallows creation of submitted contact forms.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallows deletion of submitted contact forms.
        """
        return False
