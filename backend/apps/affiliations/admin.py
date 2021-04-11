"""This module contains affiliations application configuration for the Django admin site.

This configuration allows affiliations application model instances to be viewed, created, edited, and deleted on the
Django administrator site.
"""
from django.contrib import admin

from .models import Affiliate


# Register the Affiliate model with the Django admin site.
admin.site.register(Affiliate)
