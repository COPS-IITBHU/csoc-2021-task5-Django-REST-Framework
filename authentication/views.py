from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth import login
from django.contrib.auth.models import User

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
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    
    def post(self , request):
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.save(request.data)
        token = create_auth_token(user)
        login(request, user)
        response = {
            'token' : token.key
        }
        return Response(response, status = status.HTTP_200_OK)

class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.save(request.data)
        token = create_auth_token(user)
        login(request, user)
        response = {
            'token' : token.key
        }
        return Response(response, status = status.HTTP_200_OK)



class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request):
        serializer_class = self.get_serializer(request.user)
        return Response(serializer_class.data, status = status.HTTP_200_OK)
        