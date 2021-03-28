from django.contrib.auth import views as auth_views
from django.urls import path

from store.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    ]