from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    collab_username = models.CharField(max_length=75)
    todo_id = models.IntegerField()

    def __str__(self):
        return f'{self.collab_username} - Todo ID {self.todo_id}'