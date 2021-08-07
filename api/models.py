from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Todo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
 
class collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='collaborations')
    def __str__(self):
        return self.user.username
        