from django.db.models.fields import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework import response
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
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        taskSelf=Todo.objects.filter(creator=request.user)
        taskOther = Todo.objects.filter(contributors=request.user)
        serializer1= TodoSerializer(taskSelf, many = True)
        serializer2 = TodoSerializer(taskOther, many=True)
        response=[]
        for x in serializer1.data:
            todo = Todo.objects.get(id=x['id'])
            response.append({
                'id': todo.id,
                'title': todo.title,
                'creator': todo.creator.username
            })
        for t in serializer2.data:
            todo = Todo.objects.get(id=t['id'])
            response.append({
                'id': todo.id,
                'title': todo.title,
                'creator': todo.creator.username
            })
        return Response(response,status=status.HTTP_200_OK)
        


class TodoGetSpecificView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    lookup_field = 'id'

    def put(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x = False
        for todos in queryset:
            if todos == todo:
                x = True
        if x:
            return self.update(request, id)
        else:
            return Response({"You dont have permission to edit this todo"}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x = False
        for todos in queryset:
            if todos == todo:
                x = True
        if x:
            return self.update(request, id)
        else:
            return Response({"You dont have permission to edit this todo"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"} , status=status.HTTP_404_NOT_FOUND)

        response=[]
        if todo.creator==request.user:
            response.append({
                'id': todo.id,
                'title': todo.title,
                'role': 'creator'
            })
            return Response(response, status=status.HTTP_200_OK)
        elif request.user in todo.contributors.all():
            response.append({
                'id': todo.id,
                'title': todo.title,
                'role': 'collaborator'
            })
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"You dont have permission to view this todo"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({"Todo with the following id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Todo.objects.filter(Q(creator=request.user) | Q(
            contributors=request.user))
        x = False
        for todos in queryset:
            if todos == todo:
                x = True
        if x:
            return self.destroy(request, id)
        else:
            return Response({"You dont have permission to delete this todo"}, status=status.HTTP_403_FORBIDDEN)


class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.save()
        return Response({
            "id": id,
            "title": request.data.get('title')
        }, status=status.HTTP_201_CREATED)


class TodoAddColaboratorsView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    lookup_field = 'id'

    def post(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({
                "Todo with the following id does not exists"
            }, status=status.HTTP_404_NOT_FOUND)
        if todo.creator == request.user:
            try:
                collaborator = User.objects.get(
                    username__exact=request.data.get('username'))
                if collaborator == request.user:
                    return Response({
                        "You cannot add yourself as a collaborator since you are the creator of this todo"
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    todo.contributors.add(collaborator)
                    todo.save()
            except:
                return Response({
                    "User with this username does not exists"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "You dont have permissions to add collaborators to this todo"
            }, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "Collaborator added succesfully"
        }, status=status.HTTP_200_OK)


class TodoRemoveColaboratorsView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CollaboratorSerializer
    lookup_field = 'id'

    def put(self, request, id=None):
        try:
            todo = Todo.objects.get(id__exact=id)
        except:
            return Response({
                "Todo with the following id does not exists"
            }, status=status.HTTP_404_NOT_FOUND)
        if todo.creator == request.user:
            try:
                collaborator = User.objects.get(
                    username__exact=request.data.get('username'))
                if collaborator == request.user:
                    return Response({
                        "You cannot remove yourself from collaborators since you are the creator of this todo"
                    }, status=status.HTTP_403_FORBIDDEN)
                else:
                    todo.contributors.remove(collaborator)
                    todo.save()

            except:
                return Response({
                    "User with this username does not exists"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "You dont have permissions to remove collaborators from this todo"
            }, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "Collaborator removed succesfully"
        },status=status.HTTP_200_OK)
