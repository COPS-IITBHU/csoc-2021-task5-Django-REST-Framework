from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoListSerializer,CollaboratorSerializer
from .models import Todo
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from django.db.models import Q
from django.contrib.auth.models import User

class TodoListView(ListAPIView):
    serializer_class =TodoListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self,request):
        return Todo.objects.filter(Q(creator=request.user) | Q(collaborator=request.user)).distinct()

class TodoCreateView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    queryset = Todo.objects.all()

class TodoCRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class =TodoListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self,request):
        return Todo.objects.filter(Q(creator=request.user) | Q(collaborator=request.user)).distinct()

class CollaboratorAddView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaboratorSerializer
    def post(self, request,id):
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=User.objects.get(username=serializer.initial_data['CollabUser'])
            if serializer.initial_data['CollabUser'] == request.user.username:
                return Response({'Error':'collaborator must not be user'},status=status.HTTP_400_BAD_REQUEST)
            elif user is None:
                return Response({'Error':'this user is not present'},status=status.HTTP_400_BAD_REQUEST) 
            else:
                todo[0].collaborator.add(user[0])
                todo[0].save()
                return Response({'Success':'Added collaborator successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollaboratorRemoveView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaboratorSerializer
    def delete(self, request,id):
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=User.objects.get(username=serializer.initial_data['CollabUser'])
            if serializer.initial_data['CollabUser'] == request.user.username:
                return Response({'Error':'collaborator must not be user'},status=status.HTTP_400_BAD_REQUEST)
            elif user is None:
                return Response({'Error':'this user is not present'},status=status.HTTP_400_BAD_REQUEST) 
            else:
                todo[0].collaborator.remove(user[0])
                todo[0].save()
                return Response({'Success':'Removed collaborator successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






    
