from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.db.models import Q
from .serializers import TodoCreateSerializer, TodoListSerializer, TodoEditSerializer, TodoCollabSerializer
from .models import Todo
from django.contrib.auth.models import User


def todo_editable(user, id):
    editable = False
    todo = Todo.objects.get(id=id)
    if todo.creator == user:
        editable = True
    if Todo.objects.filter(Q(id=id) & Q(collaborators__username = user.username)).exists():
        editable = True

    return editable


class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_todo = serializer.save()
        return Response(data=created_todo,status=status.HTTP_200_OK)


class TodoListView(generics.ListAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoListSerializer

    def list(self,request, *args, **kwargs):
        user = self.request.user
        serializer = TodoListSerializer(request.data)
        todos = serializer.list(user)
        return Response(data=todos, status=status.HTTP_200_OK)



class TodoEditView(generics.GenericAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class  = TodoEditSerializer

    # TODO : Handle the case when todo does not exist

    def put(self, request, *args, **kwargs):
        editable = todo_editable(request.user, kwargs.get('pk'))
        if not(editable):
            return Response(data={
                "error" : "User not authorised to edit the todo"
            },status=status.HTTP_401_UNAUTHORIZED)

        serializer = TodoEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save(kwargs.get('pk'))
        return Response(data=updated, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        editable = todo_editable(request.user, kwargs.get('pk'))
        if not(editable):
            return Response(data={
                "error" : "User not authorised to edit the todo"
            },status=status.HTTP_401_UNAUTHORIZED)

        serializer = TodoEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save(kwargs.get('pk'))
        return Response(data=updated, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        editable = todo_editable(request.user, kwargs.get('pk'))
        if not(editable):
            return Response(data={
                "error" : "User not authorised to remove the todo"
            },status=status.HTTP_401_UNAUTHORIZED)

        todo = Todo.objects.get(id=kwargs.get('pk'))
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoAddCollaborators(generics.GenericAPIView):
    # TODO : allow only when todo belongs to the user
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCollabSerializer

    def patch(self, request, *args, **kwargs):
        users = request.data.get('users')
        id = kwargs.get('pk')
        serializer = TodoCollabSerializer(request.data)

        success_message = serializer.save(id,users,'ADD')
        return Response(data=success_message, status=status.HTTP_200_OK)


class TodoRemoveCollaborators(generics.GenericAPIView):
    # TODO : allow only when todo belongs to the user
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCollabSerializer

    def patch(self, request, *args, **kwargs):
        users = request.data.get('users')
        id = kwargs.get('pk')
        serializer = TodoCollabSerializer(request.data)

        success_message = serializer.save(id,users,'DELETE')
        return Response(data=success_message, status=status.HTTP_200_OK)
    

        
