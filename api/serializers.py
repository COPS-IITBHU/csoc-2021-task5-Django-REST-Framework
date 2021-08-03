from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo


"""
TODO:
Create the appropriate Serializer class(es) for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


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
        data['id'] = todo.id

    class Meta:
        model = Todo
        fields = ('id', 'title',)

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id','title',)

class TodoAddCollabSerializer(serializers.Serializer):
    username = serializers.CharField()
    def validate(self, attrs):
        username = attrs.get('username')
        todo = self.context.get('todo')

        if username == todo.creator.username:
            raise serializers.ValidationError({
                'Creator': 'Cannot add creator of todo as a collaborator'
            })

        if username not in [i.username for i in User.objects.all()]:
            raise serializers.ValidationError({
                'username': 'Such a user does not exist'
            })
        
        if username in [i.username for i in todo.collabs.all()]:
            raise serializers.ValidationError({
                'username': 'User is already a collaborator to this todo'
            })
        return attrs

    def save(self,todo):
        newCollab = User.objects.get(username=self.validated_data.get('username'))
        self.context.get('todo').collabs.add(newCollab)

class TodoRemoveCollabSerializer(serializers.Serializer):
    username = serializers.CharField()
    def validate(self, attrs):
        username = attrs.get('username')
        todo = self.context.get('todo')

        if username == todo.creator.username:
            raise serializers.ValidationError({
                'Creator': 'Given user is creator of this todo'
            })

        if username not in [i.username for i in User.objects.all()]:
            raise serializers.ValidationError({
                'username': 'Such a user does not exist'
            })
        
        if username not in [i.username for i in todo.collabs.all()]:
            raise serializers.ValidationError({
                'username': 'User is not a collaborator to this todo'
            })
        return attrs

    def save(self,todo):
        newCollab = User.objects.get(username=self.validated_data.get('username'))
        self.context.get('todo').collabs.remove(newCollab)
