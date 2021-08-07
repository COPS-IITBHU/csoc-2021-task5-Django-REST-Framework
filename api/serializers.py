from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from authentication.serializers import *



class TodoViewSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source = 'creator.username', required = False, read_only = True)
    class Meta:
        model = Todo
        fields = ('id', 'title', 'creator')

class CollabViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False, read_only=True)
    def validate_username(self, value):
        if value != self.context['request'].user.username:
            raise serializers.ValidationError("You can't create a collab with someone else's todo")

    class Meta:
        model = collab
        fields = ('id','username','todo')

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'title',)

