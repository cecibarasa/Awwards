from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt
from django.contrib.auth.models import User

class Profile(models.Model):
    profile_picture = CloudinaryField('images')
    bio = models.TextField()
    contact = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def update_bio(self, bio):
        self.bio = bio
        self.save()

    @classmethod
    def get_profile_data(cls):
        return Profile.objects.all()

    # class Meta:
    #     db_table = 'profiles'

class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()
    def __str__(self):
        return self.first_name, self.last_name

class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    link = models.CharField(max_length=150)
    image = CloudinaryField('images')
    pub_date = models.DateTimeField(auto_now_add=True)
    # editor = models.ForeignKey(Profile, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    @classmethod
    def todays_awward(cls):
        today = dt.date.today()
        awwards = cls.objects.filter(pub_date__date = today)
        return awwards

    @classmethod
    def search_project_by_title(cls, search_term):
        project = cls.objects.filter(title__name__icontains=search_term)
        return project                 