from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime as dt
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import *

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
    post = Project.objects.get(title=post)
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rate.objects.filter(post=post)

            design_ratings = [i.design for i in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [i.usability for i in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [i.content for i in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()

    else:
        form = RatingsForm()
    data = {
        'post': post,
        'rating_form': form

    }
    return render(request, 'projects.html', data)

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
    # print("profile", profile)
   
    profile_data = {
        'profile': profile
    }
    return render(request, 'profile/profile.html', profile_data)

@login_required(login_url='login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'profile/edit_profile.html', params)

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


def rate(request):
    ratings = Rate.objects.all()
    rate_params = {
        'ratings': ratings
    }

    return render('projects.html', rate_params)    