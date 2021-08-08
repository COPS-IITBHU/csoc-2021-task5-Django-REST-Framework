from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, data):
        data = self.validated_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        return user

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=128, required=True)
    last_name = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def create(self, data):
        data = self.validated_data
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        username = data['username']
        password = data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user = authenticate(username=username, password=password)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id','first_name','last_name','username','email'] 