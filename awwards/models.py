from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from cloudinary.models import CloudinaryField
import datetime as dt


class Profile(models.Model):
    profile_picture = CloudinaryField('image')
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(default="bio")
    contact = models.CharField(max_length=200, blank=True)
    profile_Id = models.IntegerField(default=0)
    all_projects = models.ForeignKey('Project', on_delete=models.PROTECT, null=True)

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

    class Meta:
        db_table = 'profiles'


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    link = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    image = CloudinaryField('image')
    user_project_id = models.IntegerField(default=0)
    design = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))), default=0)
    usability = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))), default=0)
    creativity = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))), default=0)
    content = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))), default=0)
    vote_submissions = models.IntegerField(default=0)
    # pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save_post(self):
        self.save()    

    @classmethod
    def fetch_all_images(cls):
        all_images = Project.objects.all()
        return all_images

    @classmethod
    def get_single_project(cls, project):
        project = cls.objects.get(id=project)
        return project

    @classmethod
    def search_project_by_title(cls, search_term):
        results = cls.objects.filter(title__icontains=search_term)
        return results

    def delete_comment(self):
        self.delete()    

    class Meta:
        db_table = 'projects'
        ordering = ['-id']


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='likes', null=True)
    design = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    usability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True)
    creativity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    average = models.IntegerField(default=0)

    def save_rate(self):
        self.save()

    def delete_rate(self):
        self.delete()

    class Meta:
        db_table = 'ratings'