# Generated by Django 5.0 on 2024-05-29 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0006_rename_file_size_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
