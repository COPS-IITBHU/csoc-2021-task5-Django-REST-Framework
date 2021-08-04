from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.http import HttpResponse




class Todo(models.Model):
    collaborators = JSONField(default = [], blank = True)
    title = models.CharField(max_length=100, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)



def __str__(self):
    # return HttpResponse ('title')
    return self.title