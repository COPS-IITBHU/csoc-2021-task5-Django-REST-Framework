from rest_framework import serializers
from .models import Todo
from django.contrib.auth.models import User

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
        user = self.context['request'].user
        data = self.validated_data
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        return todo
    class Meta:
        model = Todo
        fields = ('id', 'title',)


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title','iscollab','iscreator')
        extra_kwargs = {
            'iscreator': {'read_only': True},
            'iscollab': {'read_only': True}
        }

class CollabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['collaborators']