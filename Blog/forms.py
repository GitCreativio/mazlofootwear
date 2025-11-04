from django import forms

"""
Module: forms.py

This module defines form classes for the blog application, including:
- NewsletterForm: A simple form for users to subscribe to the blog newsletter by providing their email address.
"""

class NewsletterForm(forms.Form):
    """
    A form for collecting a user's email address to subscribe to the newsletter.

    Fields:
        email (EmailField): The subscriber's email address.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'newsletter-input',
            'placeholder': 'Enter your email'
        })
    )
