from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from authentication.serializers import *

class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        todo.save()

    class Meta:
        model = Todo
        fields = ('id', 'title',)
    
class TodoCreatorSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', required = False, read_only = True)
    creator_id = serializers.IntegerField(source = 'creator.id', required = False, read_only = True)
    class Meta:
        model = Todo
        fields = ('creator','creator_id')


class TodoViewSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', required = False, read_only = True)
    creator_id = serializers.IntegerField(source = 'creator.id', required = False, read_only = True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator','creator_id')

class CollaborationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = ('todo', 'collaborators')


class CollaborationViewSerializer(serializers.ModelSerializer):
    todo = serializers.CharField(source = 'todo.title', required = False, read_only = True)
    todo_id = serializers.IntegerField(source = 'todo.id', required = False, read_only = True)
    collaboration_id = serializers.IntegerField(source = 'id', required = False, read_only = True)
    class Meta:
        model = Collaboration
        fields = ('collaboration_id','todo','todo_id','collaborators',)

