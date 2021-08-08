from django.contrib import admin
from .models import Collaborator, Todo

admin.site.register(Todo)
admin.site.register(Collaborator)