from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()
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


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', required = False, read_only = True)
    creator_id = serializers.IntegerField(source = 'creator.id', required = False, read_only = True)
    class Meta:
        model = Todo
        fields = ('title','id', 'creator', 'creator_id')


class CollabViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    todo = TodoSerializer(many=True, read_only=True)
    class Meta:
        model = collab
        fields = ('id','username','todo','todo')


# class CollabSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     def validate_username(self, value):
#         if value != self.context['request'].user.username:
#             raise serializers.ValidationError("You can't create a collab with someone else's todo")
#         return {'id', 'username', 'todo'}
    
#     class Meta:
#         model = collab
#         fields = ('id','username','todo',)
#         print(id)
