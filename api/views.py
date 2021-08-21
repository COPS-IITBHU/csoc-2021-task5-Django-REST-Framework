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

class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

class CollaborationListViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaborationViewSerializer
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        return Collaboration.objects.all()

class CollaborationUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaborationUpdateSerializer
    http_method_names = ['put', 'patch']
    
    def get_queryset(self):
        return Collaboration.objects.all()


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoViewSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Todo.objects.all()

class CollaborationUpdateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaborationUpdateSerializer
    
    def get_queryset(self):
        return Collaboration.objects.all()

