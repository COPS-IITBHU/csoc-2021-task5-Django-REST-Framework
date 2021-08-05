from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer,check,loginuser,logoutuser)


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
    serializer_class=LoginSerializer

    def get(self,request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        user=check(request.data)
        # print(user)
        if user is not None:
            token=create_auth_token(user)
            content={
                'token': token.key
            }
            loginuser(request)
            return Response(content, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """
    queryset = User.objects.all()
    serializer_class=RegisterSerializer
    
    def get(self,request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=check(request.data)
            if user is None:
                user=serializer.save()
                token=create_auth_token(user)
                content={
                    'token': token.key
                }
                loginuser(request)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_226_IM_USED)
        else:    
            return Response(status=status.HTTP_409_CONFLICT)


class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    serializer_class=UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):        
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            content={
                "id":  serializer.data['id'],
                "name":  serializer.data['first_name']+" "+serializer.data['last_name'],
                "email":  serializer.data['email'],
                "username":  serializer.data['username']
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
