from django.db.models.fields import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoGetView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    # serializer_class = TodoSerializer
    # queryset = Todo.objects.all()
    # lookup_field = 'id'

    def get(self, request):
        queryset = Todo.objects.filter(Q(creator=request.user) |  Q(
            contributors=request.user))
        # queryset = Todo.objects.filter(creator__exact=request.user)
        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data)


class TodoGetSpecificView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    lookup_field = 'id'

    def put(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"})
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x=False
        for todos in queryset:
            if todos==todo:
                x=True
        if x:
            return self.update(request, id)
        else:
            return Response({"You dont have permission to edit this todo"})
        

    def patch(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"})
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x = False
        for todos in queryset:
            if todos == todo:
                x = True
        if x:
            return self.update(request, id)
        else:
            return Response({"You dont have permission to edit this todo"})
        

    def get(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"})
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x = False
        for todos in queryset:
            if todos == todo:
                x = True
        if x:
            return self.retrieve(request)
        else:
            return Response({"You dont have permission to view this todo"})
        

    def delete(self, request, id):
        try:
            todo = Todo.objects.get(id__exact= id)
        except:
            return Response({"Todo with the following id does not exist"})
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x=False
        for todos in queryset:
            if todos==todo:
                x=True
        if x:
            return self.destroy(request, id)
        else:
            return Response({"You dont have permission to delete this todo"})


class TodoCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        return self.create(request)
        """
        Creates a Todo entry for the logged in user.
        """
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(status=status.HTTP_200_OK)


class TodoAddColaboratorsView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    lookup_field = 'id'

    def post(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({
                "Todo with the following id does not exists"
            })
        if todo.creator == request.user:
            try:
                collaborator = User.objects.get(
                    username__exact=request.data.get('username'))
                if collaborator == request.user:
                    return Response({
                        "You cannot add yourself as a collaborator since you are the creator of this todo"
                    })
                else:
                    todo.contributors.add(collaborator)
                    todo.save()
            except:
                return Response({
                    "User with this username does not exists"
                })
        else:
            return Response({
                "You dont have permissions to add collaborators to this todo"
            })

        # //queryset = User.objects.get(username__exact=request.data.get('username'))
        # //todo = Todo.objects.get(id__exact=id)
        # //serializer = CollaboratorSerializer(queryset)
        # queryset = todo
        # serializer = TodoSerializer(queryset)
        # return Response(serializer.data)
        return Response({
            "Collaborator added succesfully"
        })


class TodoRemoveColaboratorsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    lookup_field = 'id'

    def put(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({
                "Todo with the following id does not exists"
            })
        if todo.creator == request.user:
            try:
                collaborator = User.objects.get(
                    username__exact=request.data.get('username'))
                if collaborator == request.user:
                    return Response({
                        "You cannot remove yourself from collaborators since you are the creator of this todo"
                    })
                else:
                    todo.contributors.remove(collaborator)
                    todo.save()

            except:
                return Response({
                    "User with this username does not exists"
                })
        else:
            return Response({
                "You dont have permissions to remove collaborators from this todo"
            })

        return Response({
            "Collaborator removed succesfully"
        })
