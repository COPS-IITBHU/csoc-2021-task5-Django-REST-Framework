from django.http.response import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Todo
from django.contrib.auth.models import User


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
        response = serializer.save()
        return Response(response,status=status.HTTP_200_OK)

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self, request):
        task1 = Todo.objects.filter(creator=request.user)
        task2 = Todo.objects.filter(collaborator=request.user)
        serializer1 = self.get_serializer(task1, many = True)
        serializer2 = self.get_serializer(task2, many = True)
        response = []
        for t in serializer1.data:
            response.append(t)
        for x in serializer2.data:
            task = Todo.objects.get(id = x['id'])
            response.append({'id' : task.id , 'title' : task.title , 'Todo_creator' : task.creator.username})

        return Response(response, status = status.HTTP_200_OK)

class TodoCrudView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self,request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        if request.user == task.creator:
            serializer = self.get_serializer(task,many = False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.user in task.collaborator.all():
            serializer = self.get_serializer(task,many = False) 
            response = []
            response.append({'id' : task.id , 'title' : task.title , 'Todo_creator' : task.creator.username})
            return Response(response, status = status.HTTP_200_OK)
        else:
            return Response("You are not allowed to get this task",status=status.HTTP_404_NOT_FOUND)

    def put(self, request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        if request.user==task.creator or request.user in task.collaborator.all():
            serializer = self.get_serializer(task,many=False, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("You cannot edit this task",status=status.HTTP_404_NOT_FOUND)

    def patch(self, request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        if request.user==task.creator or request.user in task.collaborator.all():
            serializer = self.get_serializer(task,many=False, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("You cannot edit this task",status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        if request.user==task.creator or request.user in task.collaborator.all():
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)   
        else:
            return Response("You cannot delete this task",status=status.HTTP_404_NOT_FOUND)   

class AddCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer

    def post(self,request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        
        if task.creator == request.user:
            try:
                user = User.objects.get(username=request.data.get('collaborator_username'))
                if user in task.collaborator.all():
                    return Response("This user is already a Collaborator in this task",status=status.HTTP_404_NOT_FOUND)
                elif user==task.creator:
                    return Response("You are already creator of this Task",status=status.HTTP_404_NOT_FOUND)
                else:
                    task.collaborator.add(user)
                    task.save()
                    return Response("Collaborator Added Successfully",status=status.HTTP_200_OK) 
            except User.DoesNotExist:
                msg = ('User with this username does not exist')
                raise serializers.ValidationError(msg, code='todo')  
        else:
            msg = ('You are not the creator of this task')
            raise serializers.ValidationError(msg, code='todo')

class RemoveCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer

    def put(self,request,id):
        try:
            task = Todo.objects.get(id = id)
        except Todo.DoesNotExist:
            msg = ('Task with this Id does not exist')
            raise serializers.ValidationError(msg, code='todo')
        
        if task.creator == request.user:
            try:
                user = User.objects.get(username=request.data.get('collaborator_username'))
                if user in task.collaborator.all():
                    task.collaborator.remove(user)
                    task.save()
                    return Response("Collaborator Removed Successfully",status=status.HTTP_200_OK) 
                elif user==task.creator:
                    return Response("You are already creator of this Task",status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response("This user is not a Collaborator of this task",status=status.HTTP_404_NOT_FOUND)
                
            except User.DoesNotExist:
                msg = ('User with this username does not exist')
                raise serializers.ValidationError(msg, code='todo')  
        else:
            msg = ('You are not the creator of this task')
            raise serializers.ValidationError(msg, code='todo')

  
