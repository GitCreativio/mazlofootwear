from django.urls import path
from . import views

"""
Module: about/urls.py

This module defines URL patterns for the "About" section of the site,
mapping URL paths related to the about page to their corresponding view function.
"""

urlpatterns = [
    path(
        'about/',
        views.about,
        name='about'
    ),  # Renders the About page with company or site information
]
