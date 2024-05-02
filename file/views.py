import os
from json import loads

from django.http import (
    FileResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)

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
