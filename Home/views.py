from django.shortcuts import render
from django.core.cache import cache
from .models import (
    Category, 
    NewArrivalBanner, 
    FeaturedCollection, 
    HeroBanner, 
    StyleJournal
)

CACHE_TTL = 60 * 60 * 24  # Cache time-to-live in seconds (24 hours)

def index(request):
    """
    Render the homepage with categories, new arrival banners, hero banners,
    featured collections, and style journals.
    Uses Django's low-level cache API to optimize database queries and rendering.
    """
    # Try to get cached data
    cached_context = cache.get('index_page_context')
    
    if cached_context is None:
        # Cache miss: fetch from database
        categories = Category.objects.filter(order__gt=0).order_by('order')
        newarrivalbanner = NewArrivalBanner.objects.all()
        herobanner = HeroBanner.objects.all()
        collections = FeaturedCollection.objects.order_by('-created_at')[:6]
        journals = StyleJournal.objects.order_by('-created_at')[:3]
        
        cached_context = {
            'categories': categories,
            'newarrivalbanner': newarrivalbanner,
            'collections': collections,
            'herobanner': herobanner,
            'journals': journals,
        }
        
        # Save context in cache
        cache.set('index_page_context', cached_context, CACHE_TTL)
    
    return render(request, 'index.html', cached_context)

def privacy(request):
    """
    Render the privacy policy page.
    Caches the rendered HTML content to improve performance.
    """
    cached_html = cache.get('privacy_page_html')
    if cached_html is None:
        # Render and cache the HTML output
        cached_html = render(request, 'privacy.html').content
        cache.set('privacy_page_html', cached_html, CACHE_TTL)
    
    # Return HttpResponse with cached HTML content
    from django.http import HttpResponse
    return HttpResponse(cached_html)
