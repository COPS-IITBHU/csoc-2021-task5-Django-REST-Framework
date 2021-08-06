from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User
from django.db.models import Q


def append_to_serializer(todo, serialized_todos, room):
    collabs = []
    for collab in todo.collaborators.all():
        collabs.append(collab.username)

    serialized_todos[room].append({
        "id" : todo.id,
        "creator" : todo.creator.username,
        "title" : todo.title,
        "collaborators" : collabs
    })


class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self):
        data = self.validated_data
        user = self.context["request"].user
        title = data["title"]
        todo = Todo.objects.create(creator=user, title=title)
        todo.save()
        return {
            "id" : todo.id,
            "title" : todo.title,
        }
    
    class Meta:
        model = Todo
        fields = ("id", "title",)


class TodoListSerializer(serializers.ModelSerializer):
    def list(self,user):
        todosCreated = Todo.objects.filter(Q(creator = user)).all()
        todosCollaborating = Todo.objects.filter(Q(collaborators__username = user.username)).all()
        serialized_todos = {
            "created" : [],
            "collaborating" : [],
        }

        for todo in todosCreated:
            append_to_serializer(todo, serialized_todos, 'created')

        for todo in todosCollaborating:
            append_to_serializer(todo, serialized_todos, 'collaborating')
        
        return serialized_todos

    class Meta:
        model = Todo
        fields = ("id", "title",)


class TodoEditSerializer(serializers.ModelSerializer):    
    def pre_check(self, user, id):
        if not Todo.objects.filter(id=id).exists():
            return {
                "detail": f'Todo with id {id} does not exist!',
                "can_access": False
            }
        
        todo = Todo.objects.get(id=id)
        if todo.creator == user:
            return {
                "can_access": True
            }
            
        if Todo.objects.filter(Q(id=id) & Q(collaborators__username = user.username)).exists():
            return {
                "can_access": True
            }
        
        return {
            "detail": "User not authorised to access the todo!",
            "can_access": False
        }
        

    def fetch(self, id):
        todo = Todo.objects.get(id=id)

        collabs = []
        for collab in todo.collaborators.all():
            collabs.append(collab.username)
        
        serialized_todo = {
            "id" : todo.id,
            "creator" : todo.creator.username,
            "title" : todo.title,
            "collaborators" : collabs
        }

        return serialized_todo


    def save(self, id):
        title = self.validated_data.get("title")
        todo = Todo.objects.get(id=id)
        todo.title = title
        todo.save()
        return {
            "id" : id,
            "title" : title,
        }

    class Meta:
        model = Todo
        fields = ("id", "title",)


class TodoCollabSerializer(serializers.Serializer):
    def pre_check(self, user, id):
        if not Todo.objects.filter(id=id).exists():
            return {
                "detail": f'Todo with id {id} does not exist',
                "can_access": False,
            }
        
        todo = Todo.objects.get(id=id)
        if todo.creator == user:
            return {
                "can_access": True,
            }
        
        return {
            "detail": "User not authorized to modify collaborators!",
            "can_access": False,
        }

    def save(self,id,users,method):

        todo = Todo.objects.get(id=id)
        non_existant = []

        for username in users:
            if not(User.objects.filter(username=username).exists()):
                non_existant.append(username)
                continue

            user = User.objects.get(username=username)
            if method == 'ADD':
                todo.collaborators.add(user)
            else:
                todo.collaborators.remove(user)

        todo.save()

        error_message = None
        if len(non_existant)>0:
            error_message = "Users "
            for user in non_existant:
                error_message = error_message + user + ", "
            error_message = error_message + "were not found! Rest were "

        success_message = None
        if method == 'ADD':
            success_message = "Added Successfully!"
            if error_message is not None:
                error_message = error_message + "added!"
        else:
            success_message = "Removed Successfully!"
            if error_message is not None:
                error_message = error_message + "removed!"

        return {
            "message" : success_message,
            "error" : error_message
        }