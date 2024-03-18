from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from file.models import File


@login_required(login_url="/auth/login")
def homepage(request):
    username = request.user.username
    files = File.objects.filter(user=request.user)

    return render(
        request, "homepage.html", {"logo": username[0].upper(), "files": files}
    )
