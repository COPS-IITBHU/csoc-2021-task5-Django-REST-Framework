from rest_framework import serializers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

def check(data):
    return authenticate(username=data['username'], password=data['password'])

def loginuser(request):
    user=check(request.data)
    login(request, user)

def logoutuser(request):
    logout(request)

class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['id','firstname', 'lastname','username']



class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(
            required=True
            )
    last_name = serializers.CharField(
            required=True
            )
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta: 
        model = User
        fields = ['id','first_name', 'last_name','username', 'email'] 
    