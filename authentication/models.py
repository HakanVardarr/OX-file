from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from authentication.managers import UserManager


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
