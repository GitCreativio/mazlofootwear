from django.contrib import admin
from .models import Contact

"""
Module: contact/admin.py

This module registers the Contact model with the Django admin site and
customizes its admin interface to provide a read-only view of user-submitted
contact messages.

Class:
    ContactAdmin: Configuration for displaying contacts in the admin.
"""

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Contact model.

    Attributes:
        list_display (tuple): Fields displayed in the list view: id, name, email,
            phone, message, created_at.
        list_filter (tuple): Sidebar filter: created_at.
        search_fields (tuple): Fields searchable via the search box: name, email,
            phone, message.
        ordering (tuple): Default ordering of contacts: newest first by created_at.

    Methods:
        has_delete_permission: Disables deletion of contact messages.
        has_change_permission: Disables editing of contact messages.
        has_add_permission: Disables manual addition of contact messages.
    """
    list_display = ('id', 'name', 'email', 'phone', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of contact messages through the admin interface.

        Returns:
            bool: False to disable the "Delete" button.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Prevent modification of contact messages through the admin interface.

        Returns:
            bool: False to disable the "Change" button.
        """
        return False

    def has_add_permission(self, request, obj=None):
        """
        Prevent manual addition of contact messages through the admin interface.

        Returns:
            bool: False to disable the "Add" button.
        """
        return False
