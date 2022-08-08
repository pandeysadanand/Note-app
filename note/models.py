from django.db import models

from user.models import User


class Note(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField()
    is_archive = models.BooleanField(default=False)
    collaborator = models.ManyToManyField(User, related_name='collaborator')

    def __str__(self):
        return self.title