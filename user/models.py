from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(default=True)
    location = models.CharField(max_length=200, default=True)
    is_verified = models.BooleanField(default=False)


class LoginData(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
