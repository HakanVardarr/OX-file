# Generated by Django 5.0 on 2024-03-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0004_alter_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_size',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
