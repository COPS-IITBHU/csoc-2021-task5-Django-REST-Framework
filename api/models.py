from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Todo(models.Model):
#it is a todo created by the creator(user)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
 
class Collaboration(models.Model):
#a single todo can have multiple collaborators
    collaborators = models.ManyToManyField(User, null=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return self.todo.title

