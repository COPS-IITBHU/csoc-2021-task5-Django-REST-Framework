from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title')




class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title')
    



class TodoCollaboratorsSerializer(serializers.Serializer):
    usernames = serializers.CharField()




class TodoCreateSerializer(serializers.ModelSerializer):
    def save(self):
        data = self.validated_data
        user = self.context['request'].user
        title = data['title']
        todo = Todo.objects.create(creator=user, title=title)
        return {
            "id": todo.id,
            "title": todo.title
        }
    

    
    class Meta:
        model = Todo
        fields = ('id', 'title',)
