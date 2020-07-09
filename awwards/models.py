from django.db import models
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    profile_picture = CloudinaryField('images')
    bio = models.TextField()
    contact = models.CharField(max_length=100, blank=True)
    
class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    link = models.CharField(max_length=150)
    image = CloudinaryField('images')

    def __str__(self):
        return self.title          