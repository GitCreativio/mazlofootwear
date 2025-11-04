from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from model_utils import FieldTracker

"""
Module: models.py

This module defines the database schema for the blog application, including:
- Blog_Category: Categories for grouping posts.
- Post: Blog post entries with content, metadata, and change-tracking.

The models include field tracking to support efficient cache invalidation.
"""

class Blog_Category(models.Model):
    """
    Represents a category to which blog posts can belong.

    Attributes:
        name (CharField): The display name of the category.
        slug (SlugField): URL-friendly, unique identifier for the category.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    # Track changes for cache invalidation
    tracker = FieldTracker(fields=['slug', 'name'])
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ('name',)
        
    def __str__(self):
        """
        Return the human-readable name of the category.
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Construct the URL for the category detail view.
        
        Returns:
            str: The URL path to this category's page.
        """
        return reverse('category_posts', args=[self.slug])
    

class Post(models.Model):
    """
    Represents an individual blog post entry.

    Attributes:
        title (CharField): The title of the post.
        slug (SlugField): Unique slug per publish date, used in URLs.
        category (ForeignKey): The category this post belongs to.
        content (TextField): The full body of the post.
        excerpt (TextField): A short summary of the post.
        featured_image (ImageField): Image displayed with the post.
        publish_date (DateTimeField): When the post goes live.
        is_featured (BooleanField): Marks post as featured if True.
        author (ForeignKey): The user who wrote the post.
        tracker (FieldTracker): Utility for tracking field changes.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='publish_date')
    category = models.ForeignKey(Blog_Category, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='blog_img/', null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Track changes on specified fields for cache invalidation
    tracker = FieldTracker(fields=['category_id', 'publish_date', 'is_featured', 'title', 'slug'])

    class Meta:
        ordering = ('-publish_date',)
        verbose_name_plural = 'Posts'
        
    def __str__(self):
        """
        Return the title of the post.
        """
        return self.title
        
    def get_absolute_url(self):
        """
        Construct the URL for the post detail view based on its publish date and slug.

        Returns:
            str: The URL path to this post's detail page.
        """
        return reverse('post_detail', args=[
            self.publish_date.year,
            self.publish_date.month,
            self.publish_date.day,
            self.slug
        ])
        
    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one featured post exists at a time.
        
        If this post is being set as featured, unfeature all other posts.
        """
        if self.is_featured and not self.tracker.previous('is_featured'):
            # If this post is being set as featured and wasn't before
            # Unfeature all other posts
            Post.objects.filter(is_featured=True).exclude(pk=self.pk).update(is_featured=False)
            
        super().save(*args, **kwargs)