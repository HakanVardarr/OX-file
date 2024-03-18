from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from file.models import File


@login_required(login_url="/auth/login")
def homepage(request):
    email = request.user.email
    files = File.objects.filter(user=request.user)

    return render(request, "homepage.html", {"logo": email[0].upper(), "files": files})
