from rest_framework import serializers
from .models import Todo, collaboratorOfTodo
from django.contrib.auth.models import User


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoCreateSerializer(serializers.ModelSerializer):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        return todo
     
    class Meta:
        model = Todo
        fields = ('id', 'title',)



class TodoCollaboratorSerializer(serializers.ModelSerializer):

    def create(self, **kwargs):
        data = self.validated_data
        task = self.context["todo"]
        if (collaboratorOfTodo.objects.filter(todo = task, collaborator_username = data['collaborator_username']).exists()):
            return None

        else:    
            todoCollaborator = collaboratorOfTodo.objects.create(todo = task, collaborator_username = data['collaborator_username'], collaborator = User.objects.get(username = data['collaborator_username']))
            return todoCollaborator
        
    class Meta:
        model = collaboratorOfTodo
        fields = ('id', 'collaborator_username',)


class UserAsCollaboraterSerializer(serializers.ModelSerializer):

    class Meta:
        model = collaboratorOfTodo
        fields = ('todo',)

