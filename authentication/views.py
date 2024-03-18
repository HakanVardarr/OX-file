from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from authentication.forms import UserRegistrationForm


# Create your views here.
def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")

            User = get_user_model()
            User.objects.create_user(email=email, password=password)

            return redirect("login")

    return render(request, "register.html", {"form": form})


def login(request):
    return HttpResponse("Login page")
