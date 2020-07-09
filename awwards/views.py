from django.shortcuts import render
from django.http import HttpResponse
import datetime as dt
from . models import *

def index(request):
    awwards = Project.todays_awward()
    date = dt.date.today()
    return render(request, 'index.html', {"date":date,"awwards":awwards})     