from django.db import models
from django.contrib.auth.models import AbstractUser

USER_STATUS = (
    ("basic", "Basic"),
    ("premium", "Premium"),
    ("enterprise", "Enterprise"),
)
class CustomUser(AbstractUser):
    img_uploaded = models.ImageField(null=True, blank=True, upload_to='images/')
    status = models.CharField(choices=USER_STATUS, default="basic", max_length=30)
    def __str__(self):
        return self.username
