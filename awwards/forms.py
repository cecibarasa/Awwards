from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryFileField
from .models import *


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1", "password2"]


class PostForm(forms.ModelForm):
    image = CloudinaryFileField(
    options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
      'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
    })

    class Meta:
        model = Project
        fields = ('title', 'details', 'link', 'image')


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(
    options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
      'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
    })

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'contact']


class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['design', 'usability', 'content', 'creativity']