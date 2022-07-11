from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(default=True)
    location = models.CharField(max_length=200, default=True)
    is_verified = models.BooleanField(default=False)
