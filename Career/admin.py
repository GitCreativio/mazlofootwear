from django.contrib import admin
from .models import (
    Job,
    Application
)

"""
Module: careers/admin.py

This module registers the Job and Application models with the Django admin site
and customizes their admin interfaces for easier management of job listings and
applicant submissions.
"""

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Job model.

    Attributes:
        list_display (tuple): Fields displayed in the list view: id, title, job type,
            location, description, requirements.
        list_filter (tuple): Sidebar filters: job_type, location.
        search_fields (tuple): Fields searchable via the search box: title,
            description, requirements.
        ordering (tuple): Default ordering of jobs: alphabetical by title.
    """
    list_display = ('id', 'title', 'job_type', 'location', 'description', 'requirements')
    list_filter = ('job_type', 'location')
    search_fields = ('title', 'description', 'requirements')
    ordering = ('title',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Application model.

    Attributes:
        list_display (tuple): Fields displayed in the list view: id, job, full_name,
            email, phone_number, resume file link, cover_letter, submission_date.
        list_filter (tuple): Sidebar filters: job, submission_date.
        search_fields (tuple): Fields searchable via the search box: full_name,
            email, phone_number, resume path, cover_letter text.
        ordering (tuple): Default ordering of applications: newest first by
            submission_date.

    Methods:
        has_add_permission: Disable manual addition of Application entries
            through the admin interface.
    """
    list_display = (
        'id', 'job', 'full_name', 'email', 'phone_number',
        'resume', 'cover_letter', 'submission_date'
    )
    list_filter = ('job', 'submission_date')
    search_fields = ('full_name', 'email', 'phone_number', 'resume', 'cover_letter')
    ordering = ('-submission_date',)

    def has_add_permission(self, request, obj=None):
        """
        Prevent adding new Application entries via the admin interface.

        Returns:
            bool: False to disable the "Add" button in the admin list view.
        """
        return False
