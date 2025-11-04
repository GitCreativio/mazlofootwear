from django.shortcuts import render
from django.core.cache import cache
from .models import (
    Stat,
    Journey,
    GreenPromiseItem,
    CoreValue
)

def about(request):
    """
    Render the 'about.html' template for the About page with dynamic content.

    This view retrieves all necessary data for the About page from the database:
    - Stats: Multiple statistics to display.
    - Journey: A single object describing the company journey.
    - GreenPromiseItems: List of sustainability promises.
    - CoreValues: List of core values for the company.

    To improve performance, this data is cached in Django's cache framework
    for 15 minutes (900 seconds). Subsequent requests within this timeframe
    will be served from cache rather than querying the database again.

    Returns:
        HttpResponse: Rendered About page with dynamic context data.
    """

    # Cache timeout in seconds (24 hours)
    cache_timeout = 60 * 60 * 24

    # Attempt to fetch cached data or query DB if not cached
    stats = cache.get('about_stats')
    if stats is None:
        stats = Stat.objects.all()
        cache.set('about_stats', stats, cache_timeout)

    journey = cache.get('about_journey')
    if journey is None:
        journey = Journey.objects.first()
        cache.set('about_journey', journey, cache_timeout)

    green_promises = cache.get('about_green_promises')
    if green_promises is None:
        green_promises = GreenPromiseItem.objects.all()
        cache.set('about_green_promises', green_promises, cache_timeout)

    core_values = cache.get('about_core_values')
    if core_values is None:
        core_values = CoreValue.objects.all()
        cache.set('about_core_values', core_values, cache_timeout)

    context = {
        'stats': stats,
        'journey': journey,
        'green_promises': green_promises,
        'core_values': core_values
    }

    return render(request, 'about.html', context)
