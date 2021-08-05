from rest_framework import permissions, serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth.models import User


def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        
        authenticated_user = serializer.validated_data.get('user')
        token = create_auth_token(authenticated_user)

        return Response(data = {
            "token" : token.key,
        }, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = create_auth_token(user)

        return Response(data={
            "token" : token.key
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        user = UserSerializer(request.user)
        return Response(data=user.data, status=status.HTTP_200_OK)
