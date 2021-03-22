from django.contrib.auth import views as auth_views
from django.urls import path

from store import views

urlpatterns = [
    path('login/', views.login, name='login'),
    ]