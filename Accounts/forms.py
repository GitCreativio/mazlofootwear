"""
Forms for managing user profile information and profile picture uploads.
"""

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    """
    Form for updating basic user details such as first name, last name, and email.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfilePictureForm(forms.ModelForm):
    """
    Form for uploading or updating the user's profile picture.
    """
    class Meta:
        model = UserProfile
        fields = ['profile_picture','bio']
