from django.shortcuts import render
from django.http import HttpResponse
import datetime as dt
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def index(request):
    awwards = Project.todays_awward()
    date = dt.date.today()
    return render(request, 'index.html', {"date": date, "awwards": awwards})

def search_results(request):

    if 'awward' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search_project_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"projects": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})

def project_view(request, post):
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
    return render(request, 'index.html', data)

@login_required(login_url='login')
def profile(request, username):
    profile = Profile.objects.get(prof_user__username=request.user.username)
    print("profile", profile)
   
    profile_data = {
        'profile': profile
    }
    return render(request, 'profile.html', profile_data)

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
    return render(request, 'django-registration/registration_form.html', {'form': form})                    