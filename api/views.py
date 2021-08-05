from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TodoCreateSerializer, TodoListSerializer, CollaboratorsSerializer, TodoEditSerializer
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
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = serializer.save()
        print(s, type(s))
        return Response(s, status=status.HTTP_200_OK)


class TodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TodoListSerializer

    def get_queryset(self):
        q = Todo.objects.all()
        p = q.filter(creator=self.request.user)
        q = q.filter(collaborators=self.request.user)
        v = []
        for i in q:
            v.append(i)
        for i in p:
            if i not in v:
                v.append(i)
        return v


class Allowed(BasePermission):
    def has_object_permission(self, request, view, obj):
        t = Todo.objects.filter(id=obj.id)
        if t:
            if request.user in t[0].collaborators.all() or request.user == t[0].creator:
                return True

        return False


class TodoView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, Allowed, ]
    queryset = Todo.objects.all()
    serializer_class = TodoEditSerializer

    def get_object(self):
        q = Todo.objects.all()
        queryset1 = q.filter(creator=self.request.user)
        queryset2 = q.filter(collaborators=self.request.user)
        queryset = queryset2 | queryset1

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class AddCollaboratorView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CollaboratorsSerializer
    queryset = Todo.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        todo_id = self.kwargs.get('pk')
        user = User.objects.filter(username=request.data['collaborator'])
        if len(user) == 0:
            return Response({'Response': 'Invalid Username.'}, status=status.HTTP_400_BAD_REQUEST)

        todo = Todo.objects.filter(pk=todo_id)
        if len(todo) == 0:
            return Response({'Response': 'Invalid Id.'}, status=status.HTTP_400_BAD_REQUEST)

        if todo[0].creator != self.request.user:
            return Response({'Response': 'Only Creator can add collaborator.'}, status=status.HTTP_400_BAD_REQUEST)

        v = []
        for i in todo[0].collaborators.all():
            v.append(i.id)
        if user[0].id in v:
            return Response({'Response': 'User already in collaborator list'}, status=status.HTTP_400_BAD_REQUEST)

        v.append(user[0].id)
        todo[0].collaborators.set(v)
        todo[0].save()
        return Response({'Response': 'Success'}, status=status.HTTP_200_OK)


class RemoveCollaboratorView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CollaboratorsSerializer
    queryset = Todo.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        todo_id = self.kwargs.get('pk')
        user = User.objects.filter(username=request.data['collaborator'])
        if len(user) == 0:
            return Response({'Response': 'Invalid Username.'}, status=status.HTTP_400_BAD_REQUEST)

        todo = Todo.objects.filter(pk=todo_id)
        if len(todo) == 0:
            return Response({'Response': 'Invalid Id.'}, status=status.HTTP_400_BAD_REQUEST)

        if todo[0].creator != self.request.user:
            return Response({'Response': 'Only Creator can remove collaborator.'}, status=status.HTTP_400_BAD_REQUEST)
        v = []
        for i in todo[0].collaborators.all():
            v.append(i.id)
        if user[0].id not in v:
            return Response({'Response': 'User not present in collaborator list'}, status=status.HTTP_400_BAD_REQUEST)

        v.remove(user[0].id)
        todo[0].collaborators.set(v)
        todo[0].save()
        return Response({'Response': 'Success'},status=status.HTTP_200_OK)
