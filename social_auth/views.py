
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from  drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt
from rest_framework.response import Response
from rest_framework import status
import base64
import pyotp
from django.conf import settings
from rest_framework.permissions import AllowAny

# from ..authentication.models import User
from .serializers import FacebookSocialAuthSerializer, GoogleSocialAuthSerializer, TwitterSocialAuthSerializer

# Create your views here.
class GoogleSocialAuthView(APIView):
    
    serializer_class = GoogleSocialAuthSerializer
    
    @swagger_auto_schema(request_body=GoogleSocialAuthSerializer)
    def post(self,request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data(['auth_token'])
            
            return Response({
                'status': 'success',
                'userInfo': data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'errror',
                'message': 'Invalid token'
            },status=status.HTTP_400_BAD_REQUEST)



class FacebookSocialAuthView(APIView):
    
    serializer_class = FacebookSocialAuthSerializer
    
    @swagger_auto_schema(request_body=FacebookSocialAuthSerializer)
    def post(self,request):
        serializer = FacebookSocialAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data(['auth_token'])
            
            return Response({
                'status': 'success',
                'userInfo': data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'errror',
                'message': 'Invalid token'
            },status=status.HTTP_400_BAD_REQUEST)





class TwitterSocialAuthView(APIView):
    
    serializer_class = TwitterSocialAuthSerializer
    
    @swagger_auto_schema(request_body=TwitterSocialAuthSerializer)
    def post(self,request):
        serializer = TwitterSocialAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data(['auth_token'])
            
            return Response({
                'status': 'success',
                'userInfo': data
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'errror',
                'message': 'Invalid token'
            },status=status.HTTP_400_BAD_REQUEST)

