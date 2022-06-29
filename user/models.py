from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(default=True)
    location = models.CharField(max_length=200, default=True)


# todo title, color, is_archive, author[fk], description[text]
# todo crud operation
# todo learn FK->1-1, 1-many, many- many https://www.django-rest-framework.org/tutorial/quickstart/
