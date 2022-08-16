from django.db import models

from user.models import User


class Note(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    description = models.TextField()
    is_archive = models.BooleanField(default=False)
    collaborator = models.ManyToManyField(User, related_name='collaborator')

    def get_format(self):
        return {
            "title": self.title,
            "description": self.description
        }

    def __str__(self):
        return self.title


class Label(models.Model):
    title = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ManyToManyField(Note)

    def __str__(self):
        return self.title

    def get_label(self):
        return {"title": self.title, "color": self.color, "user_id":self.user_id}
