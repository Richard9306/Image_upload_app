# Generated by Django 4.2.5 on 2023-09-18 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("image_drf_app", "0002_customuser_status_alter_customuser_img_uploaded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="img_uploaded",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="Images",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=80)),
                ("description", models.TextField()),
                ("image_url", models.ImageField(upload_to="images/")),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]