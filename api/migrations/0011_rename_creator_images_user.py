# Generated by Django 4.2.5 on 2023-09-23 13:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_remove_images_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="images",
            old_name="creator",
            new_name="user",
        ),
    ]
