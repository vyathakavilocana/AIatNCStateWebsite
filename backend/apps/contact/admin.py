"""TODO Docs"""
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
    """TODO Docs
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
    """TODO Docs
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
        """TODO Docs
        """
        return False


@admin.register(MentorContactForm)
class MentorContactFormFormAdmin(PolymorphicChildModelAdmin):
    """TODO Docs
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
        """TODO Docs
        """
        return False


@admin.register(EventOrganizerContactForm)
class EventOrganizerContactFormAdmin(PolymorphicChildModelAdmin):
    """TODO Docs
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
        """TODO Docs
        """
        return False


@admin.register(PartnerContactForm)
class PartnerContactFormAdmin(PolymorphicChildModelAdmin):
    """TODO Docs
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
        """TODO Docs
        """
        return False


class ContactFormTypeFilter(PolymorphicChildModelFilter):
    """TODO Docs
    """
    title = _('Contact Form Type')


@admin.register(ContactFormBase)
class ContactFormBaseParentAdmin(PolymorphicParentModelAdmin):
    """TODO Docs
    """
    base_model = ContactFormBase
    child_models = (GuestSpeakerContactForm, MentorContactForm, EventOrganizerContactForm, PartnerContactForm)
    list_filter = (ContactFormTypeFilter, 'reviewed', 'ignored')

    def has_add_permission(self, request):
        """TODO Docs
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """TODO Docs
        """
        return False
