from authentication.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username
