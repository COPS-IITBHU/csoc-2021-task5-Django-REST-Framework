from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    first_name = serializers.CharField(max_length=100,required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150,required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email']

    


        
    