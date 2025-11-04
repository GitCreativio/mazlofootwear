"""
URL configuration for the shop app.

Includes:
- Shopping page with product listing and filters.
- Product detail page with variant selection.
"""

from . import views
from django.urls import path

urlpatterns = [       
    path('shopping/', views.shopping, name='shopping'),
    path('product/<int:product_id>/', views.productdetails, name='productdetails'),                     
]
