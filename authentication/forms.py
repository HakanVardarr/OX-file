from authentication.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import UserCreationForm as CreationForm


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_username(self):
        User = get_user_model()

        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class UserCreationForm(CreationForm):
    class Meta:
        model = User
        fields = ("username",)


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = ("username",)
