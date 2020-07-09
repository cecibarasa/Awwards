from django.shortcuts import render
from django.http import HttpResponse
import datetime as dt

def index(request):
    return HttpResponse('Awwards')

def awward_of_day(request):
    date = dt.date.today()
    html = f'''
        <html>
            <body>
                <h1>Awward for {day} {date.day}-{date.month}--{date.year}</h1>
            </body>
        </html>
            '''
    return HttpResponse(html)            