from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo, Collaborator
from authentication.serializers import UserSerializer

class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
    
    class Meta:
        model = Todo
        fields = ('id', 'title',)

class TodoCollabSerializer(serializers.ModelSerializer):
    collab_username = serializers.CharField(max_length=255, required=True)
    def save(self, id, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        username = data['collab_username']
        collab = User.objects.filter(username=username)[0]
        todo = Todo.objects.filter(creator=user, pk=id)[0]
        if todo:
            collaboration = Collaborator.objects.create(todo=todo, collab=collab)
            return collaboration

    class Meta:
        model = Collaborator
        fields = ('collab_username',)

