"""
URL configuration for carsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from . import views

app_name = 'django_app'

urlpatterns = [
    # path('load_template/<str:template_id>', views.load_template, name='load_template'),
    path('', views.homepage, name='homepage'),
    path('search/', views.searchView, name='search'),
    # path('template1', views.temp1, name='template1'),
    # path('template2', views.temp2, name='template2'),
    # path('template3', views.temp3, name='template3'),
    # path('template1editor', views.temp1edit, name='template1editor'),
    # path('login/', views.login_here, name='login'),
    # path('logout/', views.logout_here, name='logout'),
]
