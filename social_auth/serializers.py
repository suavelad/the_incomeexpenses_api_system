# from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from decouple  import config
# from ..authentication.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
from . import google, facebook,twitterhelper
from .register import register_social_user



class GoogleSocialAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField()
    
    
    def validate_auth_token(self,auth_token):
        user_data = google.Google.validate(auth_token)
        
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please try again',
            )
        if user_data['sub'] != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you ?')
        
        user_id = user_data['sub']
        email = user_data['email']
        try: 
            first_name,last_name = user_data['name'].split(' ') 
        except:
            first_name = last_name =  user_data['name']
        provider = 'google'
        
        return register_social_user(user_id=user_id, email=email, first_name=first_name,last_name=last_name, provider=provider)
    
    
    class Meta:
        model= User
        fields =['auth_token']
        
    
class FacebookSocialAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField()
    
    
    def validate_auth_token(self,auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        
        try:
        
            user_id = user_data['id']
            email = user_data['email']
            try: 
                first_name,last_name = user_data['name'].split(' ') 
            except:
                first_name = last_name =  user_data['name']
            provider = 'facebook'
            
            return register_social_user(user_id=user_id, email=email, first_name=first_name,last_name=last_name, provider=provider)
        
        except:
            raise serializers.ValidationError('The token is invalid or expired. please login agian.')
        
    
    class Meta:
        model= User
        fields =['auth_token']
       
    
class TwitterSocialAuthSerializer(serializers.ModelSerializer):
    access_token_key = serializers.CharField()
    access_token_secret = serializers.CharField()
    
    
    def validate(self,data):
        access_token_key = data.get('access_token_key')
        access_token_secret = data.get('access_token_secret')
        
        user_data = twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_token(access_token_key, access_token_secret)
        
        try:
        
            user_id = user_data['id_str']
            email = user_data['email']
            
            try: 
                first_name,last_name = user_data['name'].split(' ') 
            except:
                first_name = last_name =  user_data['name']
            provider = 'twitter'
            
            return register_social_user(user_id=user_id, email=email, first_name=first_name,last_name=last_name, provider=provider)
        
        except:
            raise serializers.ValidationError('The token is invalid or expired. please login agian.')
    class Meta:
        model= User
        fields =['access_token_key','access_token_secret']

    