from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
import datetime as dt
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from .forms import *
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import viewsets



def index(request):
    current_user = request.user
    date = dt.date.today()
    images = Project.fetch_all_images()
    image_params = {
        'all_images': images,
        'current_user': current_user,
        "date":date,
    }
    return render(request, "index.html", image_params)                              

def search_results(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Project.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image "
    return render(request, 'search.html', {'message': message})

def projects(request, post):
   if request.user.is_authenticated:
    user = User.objects.get(username = request.user)
    post = Project.objects.get(title = post)
    rate = Rate.objects.filter(post = post)
    design = rate.aggregate(Avg('design'))['design__avg']
    usability = rate.aggregate(Avg('usability'))['usability__avg']
    content = rate.aggregate(Avg('content'))['content__avg']
    creativity = rate.aggregate(Avg('creativity'))['creativity__avg']
    average = rate.aggregate(Avg('average'))['average__avg']
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.average = (rate.design + rate.usability + rate.content + rate.creativity) / 4
            # print(rate.average)
            rate.post = post
            rate.user = user
            rate.save()
        return redirect('project', post)
    else:
        form = RatingsForm()
    return render(request, 'projects.html', {'post': post, 'rate': rate, 'rating_form': form, 'design': design, 'usability': usability, 'content': content,'creativity':creativity, 'average':average})

def home(request):
    profile = Profile.objects.get(user_profile__username=request.user.username)
   
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    try:
        posts = Project.objects.all()
        print(posts)
    except Project.DoesNotExist:
        posts = None
    return render(request, 'index.html', {'posts': posts, 'form': form, 'profile':profile})

def signup(request):
    global register_form
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
        register_form = {
            'form': form,
        }
    return render(request, 'django_registration/registration_form.html', {'form': form})

@login_required(login_url='login')
def profile(request, username):
    profile = Profile.objects.filter(user_profile__username=request.user.username)
    
    params = {
        'profile':profile
    }
    return render(request, 'profile/profile.html', params)

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,

    }
    return render(request, 'profile/profile.html', params)

def upload(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/')
    else:
        form = PostForm()


    return render(request, 'home.html', {'form': form})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer    