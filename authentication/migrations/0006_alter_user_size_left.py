# Generated by Django 5.0 on 2024-05-02 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_size_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='size_left',
            field=models.IntegerField(default=16106127360),
        ),
    ]
