# Generated by Django 4.2.5 on 2023-09-23 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiers',
            name='tier_type',
            field=models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium'), ('enterprise', 'Enterprise')], default='basic', max_length=30),
        ),
    ]