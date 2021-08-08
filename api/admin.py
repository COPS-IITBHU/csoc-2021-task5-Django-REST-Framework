from django.contrib import admin
from .models import Todo, collaboratorOfTodo

admin.site.register(Todo)
admin.site.register(collaboratorOfTodo)