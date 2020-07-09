from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt

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
    pub_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    @classmethod
    def todays_awward(cls):
        today = dt.date.today()
        awwards = cls.objects.filter(pub_date__date = today)
        return awwards

     @classmethod
    def search_project_by_title(cls, search_term):
        project = cls.objects.filter(title__icontains=search_term)
        return project                 