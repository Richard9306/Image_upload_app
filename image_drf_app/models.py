from django.db import models
from django.contrib.auth.models import AbstractUser

USER_STATUS = (
    ("basic", "Basic"),
    ("premium", "Premium"),
    ("enterprise", "Enterprise"),
)


class CustomUser(AbstractUser):
    img_uploaded = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=USER_STATUS, default="basic", max_length=30)

    def __str__(self):
        return self.username


class Images(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField()
    image_url = models.ImageField(upload_to='images/', blank=False, null=False)

    def __str__(self):
        return self.title