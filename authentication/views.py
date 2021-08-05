from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    """
    TODO:
    Implement login functionality, taking username and password
    as input, and returning the Token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        dic = {'token': str(create_auth_token(user))}
        print(dic)
        return Response(dic, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        dic = {'token': str(create_auth_token(user))}
        print(dic)
        return Response(dic, status=status.HTTP_200_OK)


class UserProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        dic = {
            "id": user.id,
            "name": user.first_name,
            "email": user.email,
            "username": user.username
        }
        return Response(dic, status=status.HTTP_200_OK)

    """
       TODO:
       Implement the functionality to retrieve the details
       of the logged in user.
    """
