from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255, min_length=1)
    password = serializers.CharField(required=True,max_length=255, min_length=1)

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,max_length=150, min_length=1)
    email = serializers.EmailField(required=True, max_length=255, min_length=1)
    username = serializers.CharField(required=True, max_length=255, min_length=1)
    password = serializers.CharField(required=True,max_length=255, min_length=1)
    def validate(self, data):
        user = User.objects.filter(username=data['username'], email=data['email'])
        if user:
            raise serializers.ValidationError("Account already exists, please login")
        else:
            return data    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')
    