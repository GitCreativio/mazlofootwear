from django.contrib import admin
from .models import (
    Blog_Category,
    Post
)

"""
Module: admin.py

This module registers blog-related models with the Django admin site and
customizes their admin interfaces.

Classes:
    Blog_CategoryAdmin: Configuration for managing Blog_Category entries.
    PostAdmin: Configuration for managing Post entries.
"""

@admin.register(Blog_Category)
class Blog_CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Blog_Category model.

    list_display:
        Fields displayed in the list view: id, name, slug.
    list_filter:
        Filters available in the sidebar: name, slug.
    search_fields:
        Fields searched via the search box: name, slug.
    """
    list_display = ('id', 'name', 'slug')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Post model.

    list_display:
        Columns shown in the posts list: id, title, category, content,
        excerpt, featured_image, publish_date, is_featured, author.
    list_filter:
        Sidebar filters: category, publish_date, is_featured.
    search_fields:
        Searchable fields: title, content, excerpt.
    ordering:
        Default ordering of posts: newest first by publish_date.
    """
    list_display = (
        'id', 'title', 'category', 'content', 'excerpt',
        'featured_image', 'publish_date', 'is_featured', 'author'
    )
    list_filter = ('category', 'publish_date', 'is_featured')
    search_fields = ('title', 'content', 'excerpt')
    ordering = ('-publish_date',)
