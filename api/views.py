from datetime import date
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from django.http import Http404


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class TodoListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCreateSerializer

    def get(self, request):
        """
        Returns a list of all the Todos for the logged in user.
        """
        queryset = Todo.objects.filter(creator=request.user)
        response = self.get_serializer(queryset, many=True)
        print(response.data)
        return Response(response.data, status=status.HTTP_200_OK)

class TodoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            todo = Todo.objects.get(pk=pk,creator=self.request.user)
            return todo[0]

        except:
            raise Http404
    
    def get(self, request, pk):
        """
        Returns a single Todo for the logged in user.
        """
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates a Todo for the logged in user.
        """
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """
        Updates a Todo for the logged in user.
        """
        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Deletes a Todo for the logged in user.
        """
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
        return Response(serializer.data, status=status.HTTP_200_OK)
