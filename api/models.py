from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Collaborator(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    collab = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.collab.first_name +" "+ self.collab.last_name + "- " + self.todo.title