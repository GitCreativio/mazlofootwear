"""
Views for the shopping and product detail pages.
Handles product listing, filtering, sorting, and detailed product display with variants.
"""

import json
from django.shortcuts import render, get_object_or_404
from constants import *
from .models import Product
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def generate_cache_key(request):
    """Generate unique cache key based on request parameters"""
    params = [
        ','.join(sorted(request.GET.getlist('category'))),
        ','.join(sorted(request.GET.getlist('type'))),
        request.GET.get('price', ''),
        request.GET.get('sort', 'newest')
    ]
    version = cache.get('shopping_cache_version', 1)
    return f'shopping_{hash(tuple(params))}_v{version}'

@cache_page(60 * 15)  # Cache page for 15 minutes
def shopping(request):
    # Get or create static choices cache
    category_choices = cache.get_or_set(
        'category_choices',
        lambda: Product.CATEGORY_CHOICES,
        3600  # 1 hour cache
    )
    type_choices = cache.get_or_set(
        'type_choices',
        lambda: Product.TYPE_CHOICES,
        3600
    )

    # Get filtered products from cache or DB
    cache_key = generate_cache_key(request)
    products = cache.get(cache_key)
    
    if not products:
        products = Product.objects.all().prefetch_related('images')
        
        # Filtering
        selected_categories = request.GET.getlist('category')
        if selected_categories:
            products = products.filter(category__in=selected_categories)
        
        selected_types = request.GET.getlist('type')
        if selected_types:
            products = products.filter(product_type__in=selected_types)
        
        selected_price = request.GET.get('price')
        if selected_price:
            price_ranges = {
                '0-50': (0, 50),
                '50-100': (50, 100),
                '100+': (100, float('inf'))
            }
            if selected_price in price_ranges:
                products = products.filter(
                    price__range=price_ranges[selected_price]
                )

        # Sorting
        sort_options = {
            'price-asc': 'price',
            'price-desc': '-price',
            'newest': '-created_at'
        }
        products = products.order_by(sort_options.get(
            request.GET.get('sort', 'newest'), 
            '-created_at'
        ))

        # Cache evaluated queryset
        cache.set(cache_key, list(products), 900)  # 15 minutes

    context = {
        'products': products,
        'category_choices': category_choices,
        'type_choices': type_choices,
        'selected_categories': request.GET.getlist('category'),
        'selected_types': request.GET.getlist('type'),
        'selected_price': request.GET.get('price', ''),
        'selected_sort': request.GET.get('sort', 'newest'),
    }
    return render(request, 'shop.html', context)



# @cache_page(60 * 60 * 24) 
def productdetails(request, product_id):
    """
    Display detailed view of a single product with variant selection.

    Supports:
    - Displaying product images.
    - Handling color and size selection for product variants.

    Args:
        product_id (int): The ID of the product to display.

    Context:
        product (Product): The product object.
        color_data (dict): Color and size variant mapping.
        selected_color (str): Selected color code.
        selected_size (str): Selected size code.
        available_colors (list): List of available color codes.
        available_sizes (list): List of available size codes.
        product_images (QuerySet): Ordered product images.
        color_data_json (str): JSON-encoded color data for JavaScript usage.
    """
    product = get_object_or_404(Product, id=product_id)
    
    variants = product.variants.select_related('color', 'size') \
                    .order_by('color__name', 'size__code')
    product_images = product.images.all().order_by('order')

    color_data = {}
    for variant in variants:
        color = variant.color
        size = variant.size
        if color.code not in color_data:
            color_data[color.code] = {
                'name': color.name,
                'sizes': {}
            }
        color_data[color.code]['sizes'][size.code] = {
            'variant_id': variant.id,
            'stock': variant.stock,
            'size_name': str(size)
        }

    available_colors = list(variants.values_list('color__code', flat=True).distinct())
    available_sizes = list(variants.values_list('size__code', flat=True).distinct())

    selected_color = request.GET.get('color',
                        available_colors[0] if available_colors else None)
    selected_size = request.GET.get('size',
                        available_sizes[0] if available_sizes else None)

    if selected_color and not selected_size:
        sizes_for_color = variants \
            .filter(color__code=selected_color) \
            .values_list('size__code', flat=True)
        if sizes_for_color:
            selected_size = sizes_for_color[0]

    context = {
        'product': product,
        'color_data': color_data,
        'selected_color': selected_color,
        'selected_size': selected_size,
        'available_colors': available_colors,
        'available_sizes': available_sizes,
        'product_images': product_images,
        'color_data_json': json.dumps(color_data),
    }
    return render(request, 'productdetails.html', context)
