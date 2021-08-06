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

    def get(self, request, *args, **kwargs):
        serializer = TodoEditSerializer(data=request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)
        
        fetched_todo = serializer.fetch(kwargs.get('pk'))
        return Response(data=fetched_todo, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = TodoEditSerializer(data=request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)
        updated = serializer.save(kwargs.get('pk'))
        return Response(data=updated, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = TodoEditSerializer(data=request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        updated = serializer.save(kwargs.get('pk'))
        return Response(data=updated, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        serializer = TodoEditSerializer(data=request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)

        todo = Todo.objects.get(id=kwargs.get('pk'))
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoAddCollaborators(generics.GenericAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCollabSerializer

    def patch(self, request, *args, **kwargs):
        users = request.data.get('users')
        id = kwargs.get('pk')
        serializer = TodoCollabSerializer(request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)

        success_message = serializer.save(id,users,'ADD')
        return Response(data=success_message, status=status.HTTP_200_OK)


class TodoRemoveCollaborators(generics.GenericAPIView):
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCollabSerializer

    def patch(self, request, *args, **kwargs):
        users = request.data.get('users')
        id = kwargs.get('pk')
        serializer = TodoCollabSerializer(request.data)

        pre_check_res = serializer.pre_check(request.user, kwargs.get('pk'))
        if pre_check_res.get('can_access') == False:
            return Response(data=pre_check_res, status=status.HTTP_400_BAD_REQUEST)

        success_message = serializer.save(id,users,'DELETE')
        return Response(data=success_message, status=status.HTTP_200_OK)
    

        
