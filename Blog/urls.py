from django.urls import path
from . import views

"""
Module: urls.py

This module defines URL patterns for the blog application, including:
- The main blog listing view with caching and newsletter form handling.
- An AJAX endpoint to retrieve JSON data for a specific post by ID.
"""

urlpatterns = [
    path(
        'blog/',
        views.blog,
        name='blog'
    ),  # Renders the blog page with featured posts, latest posts, categories, and newsletter form
    path(
        'get-post-data/<int:post_id>/',
        views.get_post_data,
        name='get_post_data'
    ),  # Returns JSON response containing details of the specified post
]
