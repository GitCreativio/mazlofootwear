from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

"""
Module: views.py

This module defines the contact view for the application,
allowing users to send messages via a contact form.

Functions:
    contact(request): Handles rendering and processing of the contact form.
"""

def contact(request):
    """
    Display and process the contact form.

    GET requests:
        - Instantiate a blank ContactForm and render the contact page.

    POST requests:
        - Populate ContactForm with request.POST data.
        - Validate the form; if valid, save the message and add a success message.
          Redirect back to the contact page.
        - If invalid, add an error message and re-render the form with validation errors.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered contact page with form and message context.
    """
    if request.method == 'POST':    
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
