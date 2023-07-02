from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import (LoginSerializer, RegisterSerializer, UserSerializer)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate













def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token









class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data


        username = validated_data['username']
        password = validated_data['password']


        user = authenticate(request, username=username, password=password)
        if user is not None:
            return Response({
                "token": str(create_auth_token(user))
            })
        else:
            return Response({
                "User Details": "Invalid Details"
            })










class RegisterView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
        user = self.create(request, validated_data, *args, **kwargs)
        print(user.data['username'])
        user = User.objects.get(username = user.data['username'])
        return Response({'token':str(create_auth_token(user))})









class UserProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    #serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.first_name,
            "email": user.email,
        })