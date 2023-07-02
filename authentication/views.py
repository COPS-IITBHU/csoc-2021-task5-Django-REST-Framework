from rest_framework import permissions, serializers
from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
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

    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        if username=='' or password=='':
            return Response({
                'Username and password both should be provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            token = create_auth_token(user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                'non_field_errors': 
                    "Invalid credentials or the user does not exist!"
                
            }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({
                'email': 
                    "Email already exists!"
                
            },status=status.HTTP_409_CONFLICT)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username__exact=request.data.get('username'))
            token = create_auth_token(user)
            return Response({
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView, mixins.ListModelMixin):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    
    def get(self, request):
        id = request.user.id
        user = User.objects.get(id__exact=id)
        queryset = user
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
