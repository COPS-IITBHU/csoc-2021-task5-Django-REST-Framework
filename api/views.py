from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from django.http import Http404

class TodoListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCreateSerializer

    def get(self, request):

        queryset = Todo.objects.filter(creator=request.user)
        response = self.get_serializer(queryset, many=True)
        print(response.data)
        return Response(response.data, status=status.HTTP_200_OK)


class TodoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @api_view(['GET', 'PUT', 'DELETE'])

    def get_object(self, pk):
        try:
            todo = Todo.objects.get(pk=pk,creator=self.request.user)
            return todo[0]

        except:
            raise Http404
    
    def get(self, request, pk, format=None):

        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format= None):

        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):

        todo = self.get_object(pk)
        serializer = TodoViewSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk , format=None):

        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class TodoCreateView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
