from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField ( max_length=70, min_length=8, write_only=True)



    default_error_messages = {
        'username': 'The username should only contain alpanumeric characters'
    }


    class Meta:
        model = User
        fields = ['email', 'username', 'password','first_name','last_name','sex']

    
    def validate(self,data):
        email = data.get('email',' ')
        username = data.get('username',' ')
        first_name = data.get('first_name',' ')
        last_name = data.get('last_name',' ')
        sex = data.get('sex',' ')


        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)

        return data

    
    def create (self,validated_data):
        user = User.objects.create(email=validated_data['email'], username=validated_data['username'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],sex=validated_data['sex'])
        user.is_active = False
        user.is_verified = False
        user.set_password(validated_data['password'])
        user.save()
        return validated_data




class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField (max_length= 1000)

    class Meta:
        model= User
        fields =['token']
        

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField (required=True)
    password = serializers.CharField (required=True)
    
    
        
    class Meta:
        model= User
        fields =['email','password']
        

class InitiateForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    
    class Meta:
        model= User
        fields =['email']

class VerifyPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    
    
    class Meta:
        model= User
        fields =['email','code']

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    
    class Meta:
        model= User
        fields = ['password','confirm_password']
 
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField ( max_length=70, min_length=8, write_only=True)



    default_error_messages = {
        'username': 'The username should only contain alpanumeric characters'
    }


    class Meta:
        model = User
        fields = ['email', 'username', 'password','first_name','last_name','sex']

    

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)
    
    
    class Meta:
        model= User
        fields = ['old_password','new_password']
 
    