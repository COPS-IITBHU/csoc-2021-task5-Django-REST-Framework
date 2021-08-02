from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField()
    password = serializers.CharField(style = {'input_type': 'password'},write_only = True, )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username = username, password = password)

        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError("Unable to login :( !")
        return data


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    firstname = serializers.CharField()
    lastname  = serializers.CharField()
    email     = serializers.EmailField(required = True,validators = [UniqueValidator(queryset = User.objects.all())])
    username  = serializers.CharField(required = True,validators = [UniqueValidator(queryset = User.objects.all())])
    password  = serializers.CharField(style = {'input_type': 'password'}, min_length = 8,write_only = True,required = True)
    def save(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
            'id':  {'required': False, 'read_only': True}
        }

    


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model = User
        fields = ('id','username', 'email' , 'username')
    
    