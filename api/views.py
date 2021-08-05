from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer,CollaboratorCreateSerializer
from .models import Todo,Collaborator
from django.contrib.auth.models import User

"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

class TodoList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    def get(self, request):
        """
        Gets all Todos of the logged in user.
        """
        content=[]
        todo=Todo.objects.filter(creator=request.user)
        serializer=self.get_serializer(todo,many=True)
        for data in serializer.data:
            content.append(data)
        collabs=Collaborator.objects.filter(collab_name=request.user.username)
        for collab in collabs:    
            todo=Todo.objects.filter(id=collab.todo_id)
            serializer=self.get_serializer(todo,many=True)
            for data in serializer.data:
                collabtodo={
                    "id":data['id'],
                    "title":data['title'],
                    "message":"You are collaborator here!" 
                }
                content.append(collabtodo)
        return Response(content,status=status.HTTP_200_OK)

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
        todo=Todo.objects.filter(creator=request.user,title=serializer.data['title']).last()
        serializer=self.get_serializer(todo,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TodoFunctions(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    def get(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found!'},status=status.HTTP_404_NOT_FOUND)
        if todo.creator==request.user :
            serializer=self.get_serializer(todo)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)
    
    def checkuser(self,todo,user):
        if(todo.creator==user): return True
        collab = Collaborator.objects.filter(todo_id=todo.id,collab_name=user.username)
        if collab.exists(): return True
        return False
        

    def put(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found!'},status=status.HTTP_404_NOT_FOUND)
        if self.checkuser(todo,request.user):
            todo.title=request.data['title']
            todo.save()
            serializer=self.get_serializer(todo)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)

    def patch(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.checkuser(todo,request.user):
            todo.title=request.data['title']
            todo.save()
            serializer=self.get_serializer(todo)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)

    def delete(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found!'},status=status.HTTP_404_NOT_FOUND)
        if self.checkuser(todo,request.user):
            Collaborator.objects.filter(todo_id=todo.id,collab_name=request.user.username).delete()
            todo.delete()
            return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)

class CollaboratorAdder(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorCreateSerializer
    def post(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found!'},status=status.HTTP_404_NOT_FOUND)
        if todo.creator==request.user :
            try:
                user=User.objects.get(username=request.data['username'])
            except User.DoesNotExist:
                return Response({'message': 'User not found!'},status=status.HTTP_404_NOT_FOUND)
            content={
                "collab_name":request.data['username'],
                "todo_id":id
            }
            serializer = self.get_serializer(data=content)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message" : request.data['username']+" is now collaborator for your todo id "+str(id)
            },status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)
        
class CollaboratorRemover(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorCreateSerializer
    def post(self, request,id):
        todo=None
        try:
            todo=Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'message': 'Todo not found!'},status=status.HTTP_404_NOT_FOUND)
        if todo.creator==request.user :
            try:
                collab = Collaborator.objects.get(todo_id=id,collab_name=request.data['username'])
            except Collaborator.DoesNotExist:
                return Response({'message': 'Collaboration not found!'},status=status.HTTP_404_NOT_FOUND)
            collab.delete()
            return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({'message': 'You are not allowed!'},status=status.HTTP_403_FORBIDDEN)