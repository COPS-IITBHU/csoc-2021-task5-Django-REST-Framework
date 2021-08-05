from django.db.models.fields import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import TodoCreateSerializer
from .models import Todo
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoGetView(generics.GenericAPIView, mixins.ListModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    queryset = Todo.objects.all()
    lookup_field = 'id'

    def get(self, request):
        return self.list(request)


class TodoGetSpecificView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer
    queryset = Todo.objects.all()
    lookup_field = 'id'

    def put(self, request, id=None):
       return self.update(request, id)
    
    def patch(self, request, id=None):
       return self.update(request, id)

    def get(self, request, id=None):
        return self.retrieve(request)

    def delete(self, request, id):
        return self.destroy(request, id)


class TodoCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
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



