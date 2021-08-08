import re
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework import permissions
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoCollabSerializer
from api.serializers import TodoCollabSerializer
from .models import Todo, Collaborator

class TodoCreateView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = Todo.objects.filter(creator=request.user,title=serializer.data['title'])
        getTodo = self.get_serializer(instance.last())

        return Response(getTodo.data,status=status.HTTP_200_OK)

class TodoGetView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def get(self, request):
        todo=Todo.objects.filter(creator=request.user)
        serializer1=self.get_serializer(todo,many=True)
        todoCollab=Collaborator.objects.filter(collab=request.user) 
        serializer2 = []
        for collabs in todoCollab:
            temp=self.get_serializer(collabs.todo)
            serializer2.append(temp.data)
        response_data = {
            "owner": serializer1.data,
            "collaborator": serializer2
        }    
        return Response(response_data,status=status.HTTP_200_OK)

class TodoOperationsView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def get(self, request, id):
        todo = Todo.objects.filter(creator=request.user, pk=id)
        if todo:
            ownership = "owner"
            title=todo[0].title    
        else:
            todo=Todo.objects.filter(pk=id)[0]
            todoCollab=Collaborator.objects.filter(collab=request.user, todo=todo)[0] 
            ownership = "collaborator"
            title=todoCollab.todo.title
        response_data = {
            "ownership": ownership,
            "id": id,
            "title": title 
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        todo = Todo.objects.filter(creator=request.user, pk=id)
        if todo:
            todo[0].title = request.data['title']
            todo[0].save()
            serializer = self.get_serializer(todo)
        else:
            todo=Todo.objects.filter(pk=id)[0]
            todoCollab=Collaborator.objects.filter(collab=request.user, todo=todo)[0]
            todoCollab.todo.title = request.data['title']
            todoCollab.todo.save()
            serializer = self.get_serializer(todoCollab.todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        todo = Todo.objects.filter(creator=request.user, pk=id)
        if todo:
            todo[0].title = request.data['title']
            todo[0].save()
            serializer = self.get_serializer(todo)
        else:
            todo=Todo.objects.filter(pk=id)[0]
            todoCollab=Collaborator.objects.filter(collab=request.user, todo=todo)[0]
            todoCollab.todo.title = request.data['title']
            todoCollab.todo.save()
            serializer = self.get_serializer(todoCollab.todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        todo = Todo.objects.filter(creator=request.user, pk=id)
        if todo:
            todo.delete()
        else:
            todo=Todo.objects.filter(pk=id)[0]
            todoCollab=Collaborator.objects.filter(collab=request.user, todo=todo)[0]
            todoCollab.todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TodoAddCollabView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollabSerializer

    def post(self, request, id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(id=id)
        return Response(status=status.HTTP_201_CREATED)

class TodoRemoveCollabView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollabSerializer

    def post(self, request, id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = Todo.objects.filter(creator=request.user, pk=id)[0]
        collab = User.objects.filter(username=request.data['collab_username'])[0]
        Collaborator.objects.filter(todo=todo, collab=collab).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
