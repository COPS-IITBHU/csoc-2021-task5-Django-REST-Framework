from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, CollaboratorCreateSerializer
from .models import Todo, Collaborator
from django.contrib.auth.models import User


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def get(self, request):
        """
        Get all the Todos of the logged in user. Requires token in the Authorization header.
        """
        todo = Todo.objects.filter(creator=request.user)
        serializer = self.get_serializer(todo, many=True)
        todolist = serializer.data
        collabs = Collaborator.objects.filter(collab_username=request.user.username)
        for collab in collabs:
            collab_todo = {
                'id': collab.todo_id,
                'title': Todo.objects.get(id=collab.todo_id).title,
                'role': 'collaborator'
            }
            todolist.append(collab_todo)
        return Response(todolist, status=status.HTTP_200_OK)


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
        todo = serializer.save()
        response = {
            'id': todo.id,
            'title': todo.title
        }
        return Response(response, status=status.HTTP_200_OK)


class TodoView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def checkIfAllowed(self, todo, user):
        collaborator = Collaborator.objects.filter(todo_id=todo.id, collab_username=user.username).count()
        if (todo.creator == user) or collaborator:
            return True
        return False

    def get(self, request, id):
        """
        Get the Todo of the logged in user with given id. Requires token in the Authorization header.
        """
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        if self.checkIfAllowed(todo, request.user):
            serializer = self.get_serializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only creator and collaborators allowed'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        """
        Change the title of the Todo with given id, and get the new title as response. Requires token in the Authorization header.
        """
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        if self.checkIfAllowed(todo, request.user):
            todo.title = request.data['title']
            todo.save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            return Response({'error': 'Only creator and collaborators allowed'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, id):
        """
        Change the title of the Todo with given id, and get the new title as response. Requires token in the Authorization header.
        """
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
        if self.checkIfAllowed(todo, request.user):
            todo.title = request.data['title']
            todo.save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only creator and collaborators allowed'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        """
        Delete the Todo with given id. Requires token in the Authorization header.
        """
        if Todo.objects.filter(id=id).count():
            todo = Todo.objects.get(id=id)
            if self.checkIfAllowed(todo, request.user):
                Collaborator.objects.filter(todo_id=todo.id, collab_username=request.user.username).delete()
                todo.delete()
                return Response({'message': 'Todo deleted'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Only creator and collaborators allowed'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)


class CollaboratorAddView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorCreateSerializer

    def post(self, request, id):
        """
        Add a collaborator by username and todo id. Requires token in the Authorization header.
        """
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

        if todo.creator == request.user:
            if request.user.username == request.data['collab_username']:
                return Response({'error': 'User is the creator'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=request.data['collab_username']).count() == 0:
                return Response({'error': 'username does not exist'}, status=status.HTTP_404_NOT_FOUND)

            collaborator = Collaborator.objects.filter(collab_username=request.data['collab_username'], todo_id=id).count()
            if collaborator:
                return Response({'error': 'User is already a collaborator'}, status=status.HTTP_400_BAD_REQUEST)

            response = {
                "todo_id": id,
                "collab_username": request.data['collab_username']
            }
            serializer = self.get_serializer(data=response)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Only creator of todo is allowed to add collaborators'}, status=status.HTTP_403_FORBIDDEN)


class CollaboratorRemoveView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorCreateSerializer

    def post(self, request, id):
        """
        Remove a collaborator by username and todo id. Requires token in the Authorization header.
        """
        if Todo.objects.filter(id=id).count():
            todo_creator = Todo.objects.get(id=id).creator
            if request.user == todo_creator:
                if request.user.username == request.data['collab_username']:
                    return Response({'error': 'This is the creator, cannot be removed'}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    collaborator = Collaborator.objects.get(todo_id=id, collab_username=request.data['collab_username'])
                except Collaborator.DoesNotExist:
                    return Response({'error': 'No such collaborator exists for this todo'}, status=status.HTTP_404_NOT_FOUND)

                collaborator.delete()
                return Response({'message': 'Successfully Deleted'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Only creator of todo is allowed to remove collaborators'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)