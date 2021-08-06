from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self,data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError('Invalid Credentials')
        
        data['user'] = user
        return data


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self,data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'User with username {username} already exists!')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'User with email {email} already exists!')

        return data
    
    def create(self,validated_data):
        name = validated_data.get('name')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name = name
        )


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ('id','name','username','email')
