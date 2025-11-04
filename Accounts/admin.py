"""
Admin configuration for the UserProfile model.
"""

from django.contrib import admin
from .models import UserProfile

class Userprofile_Admin(admin.ModelAdmin):
    """
    Admin interface customization for the UserProfile model.
    Currently uses default settings.
    """
    pass

admin.site.register(UserProfile, Userprofile_Admin)
