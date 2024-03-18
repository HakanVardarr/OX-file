from authentication.models import User
from django.db import models
from django.utils import timezone
from file.managers import FileManager


# Create your models here.
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    filename = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(default=timezone.now)

    objects = FileManager()

    def __str__(self):
        return self.file.name
