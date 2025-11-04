"""
Module: contact/models.py

This module defines the Contact model used to store messages submitted via the contact form.

Models:
    Contact: Represents a user's message with name, email, phone, message content, and timestamp.
"""
from django.db import models

class Contact(models.Model):
    """
    Represents a message submitted by a user through the contact form.

    Fields:
        name (CharField): The name of the person submitting the message.
        email (EmailField): The email address of the sender.
        phone (CharField): Optional phone number of the sender.
        message (TextField): The content of the message.
        created_at (DateTimeField): Timestamp when the message was created.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a human-readable representation of the contact message,
        including the sender's name.
        """
        return f"Message from {self.name}"
