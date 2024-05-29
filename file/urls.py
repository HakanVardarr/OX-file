from django.urls import path

from file import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path("download", views.download, name="download"),
    path("delete", views.delete, name="delete"),
    path("share", views.share, name="share"),
    path("<str:file_name>", views.shared_file, name="shared_file"),
]
