from django.db import models
from django.utils import timezone

from authentication.models import User
from file.managers import FileManager


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    filename = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(default=timezone.now)
    size = models.IntegerField()
    public = models.BooleanField(default=False)

    objects = FileManager()

    def __str__(self):
        return self.file.name
