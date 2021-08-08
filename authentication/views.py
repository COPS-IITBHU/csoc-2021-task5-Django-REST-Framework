from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            token = create_auth_token(user)
            response_data = {"token": "Token " + str(token)}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = create_auth_token(user)
        response_data = {"token": "Token " + str(token)}
        return Response(response_data, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        response_data = {
            "id":  serializer.data['id'],
            "name": serializer.data['first_name'] + " " + serializer.data['last_name'],
            "email": serializer.data['email'],
            "username": serializer.data['username']
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
