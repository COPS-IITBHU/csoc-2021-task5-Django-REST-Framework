from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from .access import AllUsers,Creator

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
        if serializer.is_valid(raise_exception=True):
            item  = serializer.save()
            return Response({
                'id':item.id,
                'title':item.title,
            }, status=status.HTTP_201_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class TodoAllView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, AllUsers)
    
    serializer_class = TodoSerializer
   
    def list(self, request, *args, **kwargs):
        queryset1 = Todo.objects.filter(creator=request.user)
        queryset2 = Todo.objects.filter(collaborators=request.user)
        queryset = (queryset1 | queryset2).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AllUsers)    
    serializer_class = TodoSerializer
    

    def get_queryset(self):
        todocollab = Todo.objects.filter(Collaborators = self.request.user, id = self.kwargs['id'])
        if todocollab:
            todocollab[0].iscreator = False
            todocollab[0].iscollab = True
            todocollab[0].save()

        todocreator = Todo.objects.filter(creator = self.request.user, id = self.kwargs['id'])
        if todocreator:
            todocreator[0].iscreator = True
            todocreator[0].iscollab = False
            todocreator[0].save()

        return todocreator | todocollab

class AddCollab(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, Creator)
    serializer_class = CollabSerializer


    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.add_collaborators(self.kwargs['id'], request.user)
            return Response({'message': 'Success'}, status = status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Failure'}, status = status.HTTP_404_NOT_FOUND) 

class RemoveCollab(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, Creator)
    serializer_class = CollabSerializer

    def delete(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.remove_collaborators(self.kwargs['id'])
            return Response({'message': 'Success'}, status = status.HTTP_200_OK)
        else:
            return Response({'message': 'Failure'}, status = status.HTTP_404_NOT_FOUND) 