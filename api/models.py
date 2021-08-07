from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    contributors = models.ManyToManyField(
        "auth.User", verbose_name=("Contributors"))
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
