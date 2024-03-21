import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from file.models import File


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@login_required(login_url="/auth/login")
def homepage(request):
    username = request.user.username
    files = File.objects.filter(user=request.user)
    size_left = request.user.size_left

    return render(
        request,
        "homepage.html",
        {
            "logo": username[0].upper(),
            "files": files,
            "size_left": convert_size(size_left),
        },
    )
