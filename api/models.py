from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Collaborator(models.Model):
    collab_name = models.CharField(max_length=255)
    todo_id = models.SmallIntegerField()

    def __str__(self):
        return self.collab_name