"""
Models related to user profiles, including the UserProfile model and signal handlers
to ensure automatic creation and updates of user profile instances.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Extends the built-in User model to include additional profile data,
    such as a profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pic/',         
        null=True, 
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    
    """Model for storing shipping address details."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address}, {self.city}"    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, **kwargs):
    """
    Signal receiver to ensure that a UserProfile is created or updated
    whenever a User instance is saved.
    """
    UserProfile.objects.get_or_create(user=instance)
