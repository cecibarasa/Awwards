from django.db import models
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    profile_picture = CloudinaryField('images')
    bio = models.TextField
    contact = models.CharField(max_length = 100, blank=True)