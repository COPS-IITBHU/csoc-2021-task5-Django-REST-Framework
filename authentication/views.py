from django.contrib.auth.models import User
from rest_framework import permissions, serializers, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
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
    """
    TODO:
    Implement login functionality, taking username and password
    as input, and returning the Token.
    """
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({ "token": str(create_auth_token(user)) }, status=200)


class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    def post(self,request):
        serializer = RegisterSerializer(data={
            'first_name':request.data['name'],
            'email':request.data['email'],
            'username':request.data['username'],
            'password':request.data['password'],
        })
        if serializer.is_valid():
            try: 
                newUser = serializer.save()
            except :
                return Response({'username': 'This username is already taken.'}, status=400)
            return Response({ "token": str(create_auth_token(newUser)) }, status=201)
        return Response(serializer.errors,status=400)

class UserProfileView(generics.GenericAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response({
            "id":  serializer.data['id'],
	        "name":  serializer.data['first_name'],
	        "email":  serializer.data['email'],
	        "username":  serializer.data['username']
        })