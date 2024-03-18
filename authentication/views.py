from authentication.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import redirect, render


def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            User = get_user_model()
            user = User.objects.create_user(username=username, password=password)

            auth_login(request, user)
            return redirect("/")

    return render(request, "register.html", {"form": form})


def login(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("/")

            else:
                error_message = "Invalid username or password. Please try again."
                return render(
                    request,
                    "login.html",
                    {"form": form, "error_message": error_message},
                )

    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)

    return redirect("login")
