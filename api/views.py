from django.db.models import query
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.generics import *
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.http import Http404
from rest_framework.decorators import action   
from django.contrib.auth import get_user_model

# class TodoListView(generics.ListAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = TodoViewSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         uTodo = Todo.objects.filter(creator=user)
#         cTodo = collab.objects.filter(user = user).values('todo')
#         oTodo = Todo.objects.filter(pk__in = cTodo)
#         return uTodo | oTodo
class CollabListViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollabViewSerializer

    def get_queryset(self):
        return collab.objects.all()
    
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoViewSerializer

    def get_queryset(self):
        return Todo.objects.all()


    # def get_object(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         return None
    #     return super().get_object()
    
    # def get_queryset(self):
    #     user = self.request.user
    #     uTodo = Todo.objects.filter(creator=user)
    #     cTodo = collab.objects.filter(user = user).values('todo')
    #     oTodo = Todo.objects.filter(pk__in = cTodo)
    #     return uTodo | oTodo




# class CollabAddView(generics.GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CollabSerializer
#     queryset = collab

#     def post(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk, creator=request.user)
#         request.data['todo'] = todo.pk
#         serializer = self.get_serializer(data=request.data)   
#         if serializer.is_valid():
#             user = get_object_or_404(User, username=serializer.data['username'])
#             contri = collab.objects.get_or_create(todo=todo, user=user)

#             return Response(status=status.HTTP_201_CREATED)

#         else: 
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# class CollabRemoveView(generics.DestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CollabSerializer
#     queryset = collab


#     def delete(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk, creator=request.user)
#         request.data['todo'] = todo.pk
#         serializer = self.get_serializer(data=request.data)
        
#         if serializer.is_valid():
#             user = get_object_or_404(User, username = serializer.validated_data['username'])
#             contri = get_object_or_404(collab, user=user, todo=todo)
#             contri.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         else: 
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

