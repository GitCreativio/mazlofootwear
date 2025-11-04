"""
URL configuration for user authentication and profile management.

Includes:
- Email-based OTP login
- OTP verification
- OTP resend
- User logout
- Profile view and update
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # Route for user login and OTP request
    path('otp_verify/', views.otp_verify, name='otp_verify'),  # Route for verifying OTP
    path('resend_otp/', views.resend_otp, name='resend_otp'),  # Route for resending OTP
    path('add-address/', views.add_address, name='add_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('logout/', views.user_logout, name='logout'),  # Route to log out the user
    path('profile/', views.profile, name='profile'),  # Route to view and update user profile
]
