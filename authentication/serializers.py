from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.ModelSerializer):
    # TODO: Implement login functionality
    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password')
        

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            msg = ('Email Id already exists')
            raise serializers.ValidationError(msg, code='authentication')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'username')
    