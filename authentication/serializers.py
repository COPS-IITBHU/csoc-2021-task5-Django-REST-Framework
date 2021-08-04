from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password','name')
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
    