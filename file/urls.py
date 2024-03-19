from django.urls import path

from file import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path("download", views.download, name="download"),
    path("delete", views.delete, name="delete"),
]
