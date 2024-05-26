from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path("homepage", views.homepage, name="homepage"),
    path("", views.main, name="main"),
]
