from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include

from .views import *
urlpatterns = [
    url('^$', views.index, name='awwards'),
    url(r'^search/', views.search_results, name='search_results'),
    path('profile/<username>/', profile, name='profile'),
    path('registration_form/', views.signup, name='signup'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)