"""
URL configuration for django_project project.

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
from .views import SignUpView

app_name = 'django_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('stockinfo/', views.stockInfo, name='stockInfo'),
    path('news/', views.news, name='news'),
    path('add_to_favourites/<int:stock_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('remove_from_favourites/<int:stock_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('favourites/', views.favourites, name='favourites')
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('login/', views.login_here, name='login'),
    # path('logout/', views.logout_here, name='logout'),
]
