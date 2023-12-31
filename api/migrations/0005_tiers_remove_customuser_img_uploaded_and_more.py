# Generated by Django 4.2.5 on 2023-09-23 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_images_thumbnail_200_images_thumbnail_400"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tiers",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("basic", "Basic"),
                            ("premium", "Premium"),
                            ("enterprise", "Enterprise"),
                        ],
                        default="basic",
                        max_length=30,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="img_uploaded",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.tiers"
            ),
        ),
    ]
