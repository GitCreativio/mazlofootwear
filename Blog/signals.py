from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Post, Blog_Category

"""
Module: signals.py

This module defines signal handlers to invalidate cache entries when blog posts
or categories are created, updated, or deleted to ensure cache consistency.
"""

def invalidate_blog_cache(keys=None):
    """
    Helper function to invalidate specific cache keys or patterns.
    
    Args:
        keys (list): List of cache keys to invalidate. If None, invalidate all blog-related cache.
    """
    if keys is None:
        # Default keys to invalidate if none specified
        keys = [
            'blog:featured_post',
            'blog:latest_posts',
            'blog:categories',
        ]
    
    for key in keys:
        cache.delete(key)


@receiver(pre_save, sender=Post)
def invalidate_post_cache_on_change(sender, instance, **kwargs):
    """
    Signal handler to invalidate relevant cache when a post is updated.
    Checks for changes in important fields to determine which cache to invalidate.
    """
    # Always invalidate the specific post's cache
    if instance.pk:
        cache.delete(f'blog:post:{instance.pk}:data')
        
        # Get the original instance to check for changes
        try:
            # If the featured status changed, we need to invalidate featured post cache
            if instance.tracker.has_changed('is_featured'):
                invalidate_blog_cache(['blog:featured_post'])
            
            # If category changed, invalidate category cache
            if instance.tracker.has_changed('category_id'):
                # Get old and new category slugs
                old_category_id = instance.tracker.previous('category_id')
                if old_category_id:
                    try:
                        old_category = Blog_Category.objects.get(id=old_category_id)
                        # Delete old category cache
                        cache.delete_pattern(f'blog:category:{old_category.slug}:*')
                    except Blog_Category.DoesNotExist:
                        pass
                
                # Delete new category cache if it exists
                if instance.category:
                    cache.delete_pattern(f'blog:category:{instance.category.slug}:*')
            
            # Always invalidate latest posts on update
            cache.delete('blog:latest_posts')
            
        except Exception as e:
            # Log error but don't block the save operation
            print(f"Error invalidating cache: {e}")


@receiver(post_save, sender=Post)
def invalidate_post_cache_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to invalidate cache when a post is created or updated.
    """
    # For new posts, we need to invalidate the latest posts list
    if created:
        invalidate_blog_cache(['blog:latest_posts'])
        
        # If the new post is featured, invalidate featured post cache
        if instance.is_featured:
            invalidate_blog_cache(['blog:featured_post'])
            
        # Invalidate category cache for this post's category
        if instance.category:
            cache.delete_pattern(f'blog:category:{instance.category.slug}:*')


@receiver(post_delete, sender=Post)
def invalidate_post_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to invalidate cache when a post is deleted.
    """
    # Delete this post's specific cache
    cache.delete(f'blog:post:{instance.pk}:data')
    
    # Always invalidate latest posts on delete
    invalidate_blog_cache(['blog:latest_posts'])
    
    # If this was a featured post, invalidate featured post cache
    if instance.is_featured:
        invalidate_blog_cache(['blog:featured_post'])
        
    # Invalidate category cache for this post's category
    if instance.category:
        cache.delete_pattern(f'blog:category:{instance.category.slug}:*')


@receiver(post_save, sender=Blog_Category)
def invalidate_category_cache_on_save(sender, instance, **kwargs):
    """
    Signal handler to invalidate cache when a category is created or updated.
    """
    # Invalidate the categories list
    cache.delete('blog:categories')
    
    # If the slug changed, we need to invalidate all caches for this category
    if instance.tracker.has_changed('slug'):
        old_slug = instance.tracker.previous('slug')
        if old_slug:
            cache.delete_pattern(f'blog:category:{old_slug}:*')
    
    # Invalidate caches for the current slug
    cache.delete_pattern(f'blog:category:{instance.slug}:*')


@receiver(post_delete, sender=Blog_Category)
def invalidate_category_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to invalidate cache when a category is deleted.
    """
    # Invalidate the categories list
    cache.delete('blog:categories')
    
    # Invalidate any cache entries for this category
    cache.delete_pattern(f'blog:category:{instance.slug}:*')