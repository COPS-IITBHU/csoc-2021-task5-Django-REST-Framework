from django.http import response
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import ( LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)
from django.contrib.auth  import authenticate


def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token

class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user is not None:
            token=create_auth_token(serializer.validated_data['username'])
            return Response({'token':token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            user.email =serializer.validated_data['email']
            user.name =serializer.validated_data['name']
            user.save()
            token=create_auth_token(serializer.validated_data['username'])
            return Response({'token':token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
