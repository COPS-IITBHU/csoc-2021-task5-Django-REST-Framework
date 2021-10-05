from django.db.models import query
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.generics import *
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.http import Http404  


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoViewSerializer
    # http_method_names = ['get', 'put', 'patch', 'delete']
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Todo.objects.all()


class CollaborationListViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaborationSerializer

    def get_queryset(self):
        return Collaboration.objects.all()

# class TodoCreateView(generics.GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated, )
#     serializer_class = TodoCreateSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.save()
#         return Response(data, status=status.HTTP_201_CREATED)

# class CollaborationUpdateViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CollaborationUpdateSerializer
#     http_method_names = ['put', 'patch']
    
#     def get_queryset(self):
#         return Collaboration.objects.all()


#super method in python
#one viewset all functionalities
#writing tests


#django queryset api
#mysql and postgresql