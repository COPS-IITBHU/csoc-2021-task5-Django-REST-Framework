from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    def save(self,data):
        user = authenticate(username=data['username'], password=data['password'])
        if(not user):
            raise serializers.ValidationError({'Error': 'Incorrect password or username!'})
        else:
            return user

    class Meta:
        model = User
        fields = ( 'username', 'password',)


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality

    def save(self, data):
        if(User.objects.filter(username=data['username']).exists()):
            raise serializers.ValidationError({'Error': 'Username already exists!'})
        else:
            user = User.objects.create_user(
                first_name = data['name'],
                email = data['email'],
                username = data['username'],
                password = data['password'],)
            return user
            
    class Meta:
        model = User
        fields = ( 'first_name', 'email', 'username', 'password',)


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ( 'id','name', 'email', 'username',)