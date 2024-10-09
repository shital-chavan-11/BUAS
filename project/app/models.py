from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    contact_no = models.CharField(max_length=15, default='Not Provided')
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    reading_preferences = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    qualification = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, default='default@example.com')
    document_upload = models.FileField(upload_to='documents/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username  # Return username for better readability


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL if using a custom user model
    date_of_birth = models.DateField(null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    reading_preferences = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username
