from django.shortcuts import render
from django.http import HttpResponse
import datetime as dt
from . models import *

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
        return render(request, 'search.html',{"message":message})         