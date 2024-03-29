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
    path('stockinfo/', views.stockInfo, name='stockInfo'),
    path('news/', views.news_list, name='news'),
    path('add_to_favourites/<int:stock_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('remove_from_favourites/<int:stock_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('favourites/', views.favourites, name='favourites'),
    path('search/', views.search, name='search'),
    path('predict/<str:ticker>/<str:days>/', views.predict, name='predict'),
    path('stock_prediction/<str:ticker>/<int:days>/',views.stock_prediction_view, name='stock_prediction_view'),
]
