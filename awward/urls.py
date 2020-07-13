"""awward URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth import views
from django.contrib.auth import views as auth_views
from django_registration.backends.one_step.views import RegistrationView
from rest_framework import routers
from awwards.views import ProfileViewSet,UserViewSet,ProfileViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('awwards.urls')),
    url('accounts/register/',
        RegistrationView.as_view(success_url='/accounts/login/'),
        name='django_registration_register'),
    url('accounts/', include('django_registration.backends.one_step.urls')),
    url('accounts/', include('django.contrib.auth.urls')),
    url("logout/", auth_views.LogoutView.as_view()),
    url(r'', include(router.urls)),
     url(r'^api-token-auth/', obtain_auth_token),
     url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
