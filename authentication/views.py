from rest_framework import permissions, serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    """
    TODO:
    Implement login functionality, taking username and password
    as input, and returning the Token.
    """
    serializer_class = LoginSerializer

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                        status=400)
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                        status=404)    
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
            "token" : token.key
        })


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.get(username=self.request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)