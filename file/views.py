import os
from json import loads

from django.contrib.auth.decorators import login_required
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import render

import file
from file.forms import UploadFileForm
from file.models import File


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user

            file_size = request.FILES["file"].size
            if user.size_left - file_size > 0:
                file = File.objects.create_file(
                    user=user, uploaded_file=request.FILES["file"]
                )

                user.size_left -= file_size
                user.save()

                return JsonResponse(
                    {
                        "filename": file.filename,
                        "uploaded_at": file.uploaded_at,
                        "size_left": user.size_left,
                    }
                )
            else:
                return HttpResponseNotAllowed("Your storage size is not enough")

    return HttpResponseNotFound()


@login_required
def download(request):
    if request.method == "POST":
        filename = loads(request.body)["filename"]
        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            try:
                file_object = File.objects.filter(filename=filename, public=True)
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
        user = request.user
        filename = loads(request.body)["filename"]

        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            return HttpResponseNotFound()

        file_path = file_object.file.path
        user.size_left += file_object.size
        user.save()

        os.remove(file_path)
        file_object.delete()

        return JsonResponse({"size_left": user.size_left})

    return HttpResponseNotFound()


def share(request):
    if request.method == "POST":
        user = request.user
        filename = loads(request.body)["filename"]

        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            return HttpResponseNotFound()

        file_object.public = True
        file_object.save()

        return JsonResponse({"file_name": file_object.filename})

    return HttpResponseNotFound()


@login_required(login_url="/")
def shared_file(request, file_name):
    try:
        file_object = File.objects.get(filename=file_name, public=True)
    except File.DoesNotExist:
        try:
            file_object = File.objects.get(filename=file_name)
        except:
            return render(request, "file_not_found.html", {"msg": "File not found."})

        return render(
            request, "file_not_found.html", {"msg": "You cannot access this file."}
        )

    return render(request, "file.html", {"file_name": file_name})


def hide(request):
    if request.method == "POST":
        filename = loads(request.body)["filename"]

        try:
            file_object = File.objects.get(user=request.user, filename=filename)
        except File.DoesNotExist:
            return HttpResponseNotFound()

        file_object.public = False
        file_object.save()

        return HttpResponse()

    return HttpResponseNotFound()
