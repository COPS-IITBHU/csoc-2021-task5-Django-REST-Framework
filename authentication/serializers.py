from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
     
    # TODO: Implement login functionality
     username = serializers.CharField(max_length=500)
     password = serializers.CharField(max_length=500)
     
     def verify(self, validated_data):
         data = validated_data
         user = authenticate(username = data['username'], password = data['password'])
         if user is not None:
             return user
         else:
             return None    


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
     name = serializers.CharField(max_length=500)
     email = serializers.CharField(max_length=500)
     username = serializers.CharField(max_length=500)
     password = serializers.CharField(max_length=500)

     def create(self, validated_data):
        data = validated_data
          
        newUser = User.objects.create_user(data['username'],data['email'],data['password'])
        newUser.first_name = data['name']
        newUser.save()
        return newUser


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name')
    