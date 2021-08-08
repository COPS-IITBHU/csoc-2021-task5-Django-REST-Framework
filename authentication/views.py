from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer
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
    serializer_class = LoginSerializer
          
    def post(self , request):
        data = request.data
        loginSerializer = LoginSerializer(data = data)
        loginSerializer.is_valid(raise_exception=True)
        user = loginSerializer.verify(data)
        if user is not None:
            token = create_auth_token(user)
            return Response({'token': token.key})
        else:
            return Response({"User credentials are incorrect."},status = status.HTTP_400_BAD_REQUEST)    



class RegisterView(generics.GenericAPIView):
    """
    TODO:
    Implement register functionality, registering the user by
    taking his details, and returning the Token.
    """

    serializer_class = RegisterSerializer
   
    
    def post(self, request):
        data = request.data
        if(User.objects.filter(email = data['email']).exists()):
            return Response({"Email already taken."}, status = status.HTTP_400_BAD_REQUEST)
        elif (User.objects.filter(username = data['username']).exists()):    
            return Response({"Username already taken."}, status = status.HTTP_400_BAD_REQUEST)
        else:    
            serializer = RegisterSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            user = serializer.create(data)
        # print(user)
            token = create_auth_token(user)
            return Response({'token': token.key})
           
         



class UserProfileView(generics.RetrieveAPIView):
    """
    TODO:
    Implement the functionality to retrieve the details
    of the logged in user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        return Response({'id' : data['id'], 'name' : data['first_name'], 'email' : data['email'], 'username' : data['username']})