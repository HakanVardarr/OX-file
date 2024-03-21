import os
from json import loads

from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from regex import P

from file.forms import UploadFileForm
from file.models import File


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user

            File.objects.create_file(user=user, uploaded_file=request.FILES["file"])

            return redirect("/")

    return HttpResponseNotFound()


def download(request):
    if request.method == "POST":
        filename = loads(request.body)["filename"]
        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            return HttpResponseNotFound()

        file_path = file_object.file.path
        try:
            return FileResponse(open(file_path, "rb"))

        except FileNotFoundError:
            return HttpResponseNotFound()

    return HttpResponseNotFound()


def delete(request):
    if request.method == "POST":
        filename = loads(request.body)["filename"]

        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            return HttpResponseNotFound()

        file_path = file_object.file.path
        print(file_path)

        os.remove(file_path)
        file_object.delete()

        return HttpResponse()

    return HttpResponseNotFound()
