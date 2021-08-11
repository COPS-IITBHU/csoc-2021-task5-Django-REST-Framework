from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.fields.related import ManyToManyField

class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 
class collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.username
        