from django.urls import path
from . import views

"""
Module: careers/urls.py

This module defines URL patterns for the careers section of the site, mapping URL paths
related to job opportunities and application pages to their corresponding view functions.
"""

urlpatterns = [
    path(
        'careers/',
        views.careers,
        name='careers'
    ),  # Renders the careers overview page where users can view and apply for open positions
]
