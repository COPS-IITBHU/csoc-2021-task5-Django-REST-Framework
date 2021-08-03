from django.http.request import QueryDict
from rest_framework import (generics, permissions, status)
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (TodoCreateSerializer, TodoSerializer,TodoAddCollabSerializer,TodoRemoveCollabSerializer)
from .models import Todo


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self,request):
        todos = Todo.objects.filter(creator=request.user)
        serializer = self.get_serializer(todos,many=True)
        return Response(serializer.data)

class TodoDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get_todo(self, id):
        try:
            return Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            raise Http404
    
    def check_user(self,todo):
        if todo.creator == self.request.user:
            return 1
        if self.request.user in todo.collabs.all():
            return 1
        return 0

    def get(self, request, id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    def put(self, request, id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoAddCollabs(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get_todo(self, id):
        try:
            return Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            raise Http404

    def check_user(self,todo):
        if todo.creator == self.request.user:
            return 1
        return 0

    def post(self,request,id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)

        serializer = TodoAddCollabSerializer(data = request.data, context={'todo':todo})      
        if serializer.is_valid():
            serializer.save(todo)
            return Response({'info': 'New Collaborator Added'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoRemoveCollabs(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get_todo(self, id):
        try:
            return Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            raise Http404

    def check_user(self,todo):
        if todo.creator == self.request.user:
            return 1
        return 0

    def post(self,request,id):
        todo = self.get_todo(id)
        if self.check_user(todo)==0:
            return Response(status=401)

        serializer = TodoRemoveCollabSerializer(data = request.data, context={'todo':todo})      
        if serializer.is_valid():
            serializer.save(todo)
            return Response({'info': 'Collaborator Removed'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
