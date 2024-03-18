from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import UserCreationForm as CreationForm

from authentication.models import User


class UserRegistrationForm(forms.Form):
    email = forms.CharField(label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        User = get_user_model()

        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class UserCreationForm(CreationForm):

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(ChangeForm):

    class Meta:
        model = User
        fields = ("email",)
