from . import views
from django.urls import path

"""
URL configuration for the app.

Defines URL patterns mapping to corresponding views:
- '' (empty path) maps to the homepage view `index`
- 'privacy/' maps to the privacy policy page view `privacy`
"""

urlpatterns = [
    path('', views.index, name='home'),        # Homepage URL
    path('privacy/', views.privacy, name='privacy'),  # Privacy policy page URL
]
