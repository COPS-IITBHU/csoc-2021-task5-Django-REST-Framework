from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from django.contrib.auth.models import User

"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""
class CustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.method == "POST"):
            return True
        todo = Todo.objects.get(id=obj.id)
        if(todo.creator == request.user or request.user in todo.collaborators.all()):
            return True
        return False

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
        response = serializer.save()
        return Response(response,status=status.HTTP_200_OK)

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListSerializer

    def get(self, request):
        queryset_cr = Todo.objects.filter(creator = request.user)
        queryset_co = Todo.objects.filter(collaborators=request.user)

        serializer_cr = self.get_serializer(queryset_cr,many=True)
        serializer_co = self.get_serializer(queryset_co,many=True)

        response = {
            "CREATOR" : 
            serializer_cr.data,
            "COLLABORATOR" :
            serializer_co.data,
        }
        return Response(response,status=status.HTTP_200_OK)
        

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView, CustomPermission):
    permission_classes = (permissions.IsAuthenticated, CustomPermission)
    serializer_class = TodoCommonSerializer
    lookup_url_kwarg = 'id'
    queryset = Todo.objects.all()


class TodoAddCollabView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCollabSerializer

    def patch(self, request, id):
        todo = Todo.objects.get(id=id)
        if(request.user == todo.creator):
            username = request.data['username']
            user = User.objects.get(username=username)
            if(user != request.user):
                todo.collaborators.add(user)
                serializer_class = self.get_serializer(todo,data=request.data)
                serializer_class.is_valid(raise_exception=True)
                return Response(serializer_class.data, status = status.HTTP_200_OK)
            return Response({"Error": "You are already the creator of this todo"}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "You are not the creator of this todo"}, status = status.HTTP_403_FORBIDDEN)
   

class TodoDeleteCollabView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollabSerializer

    def patch(self, request, id):
        todo = Todo.objects.get(id=id)
        if(request.user == todo.creator):
            username = request.data['username']
            user = User.objects.get(username=username)
            todo.collaborators.remove(user)
            serializer_class = self.get_serializer(todo,data=request.data)
            serializer_class.is_valid(raise_exception=True)
            return Response(serializer_class.data, status = status.HTTP_200_OK)
        return Response({"Error": "You are not the creator of this todo"}, status = status.HTTP_403_FORBIDDEN)