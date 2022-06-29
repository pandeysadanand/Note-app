from django.db import models

from user.models import User


class Note(models.Model):
    note_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField()
    is_archive = models.BooleanField(default=False)
