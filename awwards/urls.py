from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from .views import home, project_view, signup, profile, edit_profile, upload, index


urlpatterns = [
    url('^$', views.index, name='awwards'),
    url(r'^search/', views.search_results, name='search_results'),
    path('profile/<username>/', profile, name='profile'),
    path('registration_form/', views.signup, name='signup'),
    path('project/<post>', project_view, name='project'),
    path('upload/', views.upload, name='upload'),
    path('profile/<username>/settings', edit_profile, name='edit'),
    path('account/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)