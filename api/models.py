from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()

class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
 
class collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    todos = models.ManyToManyField(Todo, null = True)

    
    def __str__(self):
        return self.user.username

