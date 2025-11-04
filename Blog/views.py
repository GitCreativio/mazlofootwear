from constants import *
from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import Post, Blog_Category
from django.http import JsonResponse
from .forms import NewsletterForm
from django.contrib import messages
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

"""
Module: views.py

This module defines view functions for the blog application, including:
- A blog listing page with featured posts, latest posts, categories, and newsletter subscription handling.
- An AJAX endpoint to retrieve detailed data for a specific post, with core-level caching.
- Optimized caching strategies for better performance.
"""

# Cache timeout constants
HOUR = 60 * 60
DAY = HOUR * 24
LONG_CACHE = DAY  # 24 hours
MEDIUM_CACHE = HOUR * 6  # 6 hours
SHORT_CACHE = HOUR  # 1 hour


def get_featured_post():
    """
    Helper function to fetch the featured post with related models.
    Used by the cache system for lazy evaluation.
    
    Returns:
        Post object or None if no featured post exists
    """
    return Post.objects.select_related('category', 'author').filter(is_featured=True).first()


def get_latest_posts(limit=3):
    """
    Helper function to fetch the latest non-featured posts with related models.
    Used by the cache system for lazy evaluation.
    
    Args:
        limit (int): Maximum number of posts to return
        
    Returns:
        List of Post objects
    """
    return list(
        Post.objects.select_related('category', 'author')
        .filter(is_featured=False)
        .order_by('-publish_date')[:limit]
    )


def get_categories():
    """
    Helper function to fetch all blog categories.
    Used by the cache system for lazy evaluation.
    
    Returns:
        List of Blog_Category objects
    """
    return list(Blog_Category.objects.all())


def blog(request):
    """
    Render the main blog page and handle newsletter subscriptions.

    Retrieves and caches:
    - The featured post (key: 'featured_post').
    - The latest non-featured posts (key: 'latest_posts').
    - All blog categories (key: 'categories').

    Also processes POST requests for newsletter sign-up.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered blog page with context data.
    """
    # Use core caching to store/retrieve data with optimized cache keys
    featured_post = cache.get_or_set('blog:featured_post', get_featured_post, timeout=MEDIUM_CACHE)
    
    # Cache latest posts with a shorter timeout as they change more frequently
    latest_posts = cache.get_or_set('blog:latest_posts', get_latest_posts, timeout=SHORT_CACHE)
    
    # Cache categories with a longer timeout as they rarely change
    categories = cache.get_or_set('blog:categories', get_categories, timeout=LONG_CACHE)

    # Newsletter form handling
    form = NewsletterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, SUBSCRIPTION_SUCCESS)
        return redirect('blog')

    context = {
        'featured_post': featured_post,
        'posts': latest_posts,
        'categories': categories,
        'form': form,
    }
    return render(request, 'blog.html', context)


# Cache the post data view for better performance, but with a shorter timeout
@cache_page(HOUR * 2)
def get_post_data(request, post_id):
    """
    AJAX endpoint to fetch data for a given blog post.

    Checks the cache for the post data under key 'post_{post_id}_data'. If not present,
    retrieves the post, constructs a serializable dictionary, caches it, and returns as JSON.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post to retrieve.

    Returns:
        JsonResponse: A JSON response with post details or an error message if not found.
    """
    cache_key = f'blog:post:{post_id}:data'
    post_data = cache.get(cache_key)

    if not post_data:
        try:
            # Optimize query with select_related
            post = Post.objects.select_related('category', 'author').get(id=post_id)
            post_data = {
                'title': post.title,
                'content': post.content,
                'category': post.category.name,
                'author': post.author.get_full_name() or post.author.username,
                'date': post.publish_date.strftime("%B %d, %Y"),
                'image': post.featured_image.url if post.featured_image else None,
            }
            # Cache individual post data for a day
            cache.set(cache_key, post_data, timeout=DAY)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    return JsonResponse(post_data)


def category_posts(request, category_slug):
    """
    Display posts filtered by a specific category.
    
    Args:
        request (HttpRequest): The HTTP request object.
        category_slug (str): The slug of the category to filter by.
        
    Returns:
        HttpResponse: The rendered category page with filtered posts.
    """
    # Create cache key based on category and page number
    page = request.GET.get('page', 1)
    cache_key = f'blog:category:{category_slug}:page:{page}'
    
    result = cache.get(cache_key)
    
    if not result:
        try:
            # Get category with efficient query
            category = Blog_Category.objects.get(slug=category_slug)
            
            # Get posts for this category with pagination
            posts = Post.objects.select_related('category', 'author').filter(
                category=category
            ).order_by('-publish_date')
            
            # Here you would implement pagination if needed
            
            result = {
                'category': category,
                'posts': list(posts),
            }
            
            # Cache this category view for a shorter period
            cache.set(cache_key, result, timeout=SHORT_CACHE)
            
        except Blog_Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    
    # Always get fresh categories for the sidebar
    categories = cache.get_or_set('blog:categories', get_categories, timeout=LONG_CACHE)
    
    context = {
        'category': result['category'],
        'posts': result['posts'],
        'categories': categories,
        'form': NewsletterForm(),
    }
    
    return render(request, 'blog_category.html', context)