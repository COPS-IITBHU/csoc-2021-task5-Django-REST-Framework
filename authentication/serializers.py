from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(max_length=75)
    password = serializers.CharField(max_length=75, style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Unable to login with given credentials')


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=75, validators = [UniqueValidator(queryset = User.objects.all())])
    email = serializers.EmailField(max_length=100, validators = [UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(max_length=75, style = {'input_type': 'password'}, write_only=True)

    def save(self, validated_data):
        user = User.objects.create_user(first_name = validated_data['firstname'],
                                        last_name = validated_data['lastname'],
                                        username = validated_data['username'],
                                        email = validated_data['email'],
                                        password = validated_data['password']
                                        )
        return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta: 
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
    