# Generated by Django 4.2.5 on 2023-09-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_rename_name_tiers_tier_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tiers",
            name="tier_type",
            field=models.CharField(max_length=30),
        ),
    ]
