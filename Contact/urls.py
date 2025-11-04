from django.urls import path
from . import views

"""
Module: contact/urls.py

This module defines URL patterns for the contact section of the site, mapping URL paths
related to the contact form to their corresponding view functions.
"""

urlpatterns = [
    path(
        'contact/',
        views.contact,
        name='contact'
    ),  # Renders and processes the contact form for user messages
]
