import os
from secrets import token_urlsafe

from django.conf import settings
from django.db import models


class FileManager(models.Manager):
    def create_file(self, user, uploaded_file):
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        original_filename = uploaded_file.name
        unique_filename = self._change_file_name(original_filename, upload_dir)

        file = self.model(user=user, filename=unique_filename)
        file.file.save(unique_filename, uploaded_file)
        file.save()
        return file

    def _change_file_name(self, filename, upload_dir):
        name, extension = os.path.splitext(filename)

        temp_filename = os.path.join(name + "_" + token_urlsafe(16) + extension)

        while os.path.exists(temp_filename):
            temp_filename = os.path.join(
                upload_dir, name + "_" + token_urlsafe(16) + extension
            )

        return temp_filename
