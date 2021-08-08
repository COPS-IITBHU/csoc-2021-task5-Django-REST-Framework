from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class collaboratorOfTodo(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborator_username = models.CharField(max_length=500, default = "")

    def __str__(self):
        return self.todo.title 