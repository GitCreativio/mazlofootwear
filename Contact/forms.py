"""
Module: contact/forms.py

This module defines form classes for the contact application, including:
- ContactForm: A ModelForm for users to submit their contact information and message.
"""
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """
    A form for collecting user contact submissions.

    This form is based on the Contact model and includes fields for:
        - name: The sender's name.
        - email: The sender's email address.
        - phone: An optional phone number.
        - message: The content of the user's message.
    """
    class Meta:
        """
        Meta options for ContactForm to specify model, fields, and widgets.

        Attributes:
            model: The Contact model to which this form corresponds.
            fields: List of model fields included in the form.
            widgets: Custom widgets for rendering each form field with appropriate CSS classes and placeholders.
        """
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (Optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'How can we assist you?',
                'rows': 6
            }),
        }
