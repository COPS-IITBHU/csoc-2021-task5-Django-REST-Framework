from datetime import date
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from authentication.serializers import *




class TodoViewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required = False, read_only = True)
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required = False, read_only = True)

    class Meta:
        model = Todo
        fields = ('id', 'title', 'created_at', 'updated_at')


class CollabViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    todo = serializers.CharField(source = 'todo.title', required=False, read_only=True)
    todo_id = serializers.CharField(source='todo.id', required=False, read_only=True)
    creator = serializers.CharField(source = 'creator.username',required =False,  read_only=True)

    def validate_username(self, value):
        if value != self.context['request'].user.username:
            raise serializers.ValidationError("You can't create a collab with someone else's todo")
    class Meta:
        model = collab
        fields = ('id', 'username', 'todo', 'todo_id','creator')
    



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
