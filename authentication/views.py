from rest_framework import permissions, serializers
from rest_framework import generics
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib import auth
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)




class LoginView(generics.GenericAPIView):
    """
    TODO:
    Implement login functionality, taking username and password
    as input, and returning the Token.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.get_token()
        return Response(response.data, status=status.HTTP_200_OK)



class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        return Response(response.data, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer.get_serializer(request.user)
        return Response(serializer.data)