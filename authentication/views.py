# from income_expenses_project.authentication.models import User
from django.utils.http import urlsafe_base64_encode
from .models import User
from django.shortcuts import render
from  rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import authenticate,login, logout
from django.conf import settings
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





from .serializers import UserSerializer, EmailVerificationSerializer,LoginSerializer,\
    InitiateForgotPasswordSerializer,VerifyPasswordResetSerializer,ResetPasswordSerializer,ChangePasswordSerializer
from .utils import SendEmail,generateKey
from .tokens import account_activation_token


# Create your views here.
class RegisterUserView(APIView):
    serializer_class = UserSerializer
    permission_classes= (AllowAny,)


    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            
            user_data = serializer.data
            email= user_data['email']
            user = User.objects.get(email=email)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            keygen=generateKey()
            print('keygen:',keygen)
            key = base64.b32encode(keygen.returnValue(email).encode())
            OTP = pyotp.TOTP(key, interval= settings.OTP_TIMEOUT)
            print(str(OTP.now()))
            d_token= str(OTP.now())
            
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            url = 'http://'+current_site+relative_link+'?u='+(uid)+'.'+str(d_token)
            main_url = 'http://'+current_site+relative_link+'?token='+str(token)

            # email_body = 'Hi '+ user.first_name  + ' ' + user.last_name + '\n, Use the link below to verify your email  \n' + main_url
            email_body = 'Hi '+ user.first_name  + ' ' + user.last_name +','+ '\n Use the link below to verify your email:  \n' + url
            data = {'email_body':email_body,'to_email':email,'email_subject':'Email Verification'}
            # SendEmail.send_email(data)
            
            print('Mail Sent')
            
            return Response({'data':user_data},status=status.HTTP_201_CREATED)
        
        else:
            default_errors = serializer.errors
        new_error = {}
        for field_name, field_errors in default_errors.items():
            new_error[field_name] = field_errors[0]
        return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
            #  return Response({'error':'Invalid Data Passed'},status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

  
            
#   Verification with otp and uid
class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes= (AllowAny,)
    
    token_param_config = openapi.Parameter(
        'code', in_=openapi.IN_QUERY, description='link sent via email for verification (the link is mostly clicked)', type = openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        code = request.GET.get('u')
        uidb64,token = code.split('.')
        print (uidb64,token)
        
        try:
           
            uid = force_text(urlsafe_base64_decode(uidb64))
            print ('user:',uid)
            
            keygen= generateKey()
            user = User.objects.get(id=uid)

            key=base64.b32encode(keygen.returnValue(user.email).encode())
            OTP= pyotp.TOTP(key, interval=settings.OTP_TIMEOUT)
            
            
            print('user:',user.id, ' token:',OTP.verify(token))
            
            # print ('status:',account_activation_token.check_token(user, str(token)))
            if user is not None :
                
                # if account_activation_token.check_token(user, str(token)) :
                if OTP.verify(token):
                
                    if not user.is_verified  :
                        user.is_verified = True
                        user.is_active = True
                        user.save()
                    
                        return Response({
                            'status':'success',
                            'email': ' Successfully Activated'})
                    else:
                        return Response({
                            'status':'error',
                            'email': 'User is already verified'},status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        'status':'error',
                        'email': 'Link is no longer valid'},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'status':'error',
                    'email': ' User does not exist'},status=status.HTTP_401_UNAUTHORIZED)
                
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link  Expired'},status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': ' Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
      


          
# #   Verification with custom token and uid
# class VerifyEmailView(APIView):
#     serializer_class = EmailVerificationSerializer
    
#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='token for email verification', type = openapi.TYPE_STRING)
    
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self,request):
#         code = request.GET.get('u')
#         uidb64,token = code.split('.')
#         print (uidb64,token)
        
#         try:
           
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             print ('user:',uid)
            
#             user = User.objects.get(id=uid)
#             print('user:',user.id)
            
#             print ('status:',account_activation_token.check_token(user, str(token)))
#             if user is not None :
                
#                 if account_activation_token.check_token(user, str(token)) :
                
#                     if not user.is_verified  :
#                         user.is_verified = True
#                         user.is_active = True
#                         user.save()
                    
#                         return Response({
#                             'status':'success',
#                             'email': ' Successfully Activated'})
#                     else:
#                         return Response({
#                             'status':'error',
#                             'email': 'User is already verified'},status=status.HTTP_401_UNAUTHORIZED)
#                 else:
#                     return Response({
#                         'status':'error',
#                         'email': 'Link is no longer valid'},status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 return Response({
#                     'status':'error',
#                     'email': ' User does not exist'},status=status.HTTP_401_UNAUTHORIZED)
                
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Link  Expired'},status=status.HTTP_400_BAD_REQUEST)
        
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': ' Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
      
# Using access token
# class VerifyEmailView(APIView):
#     serializer_class = EmailVerificationSerializer
    
#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='token for email verification', type = openapi.TYPE_STRING)
    
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self,request):
#         token = request.GET.get('token')
        
#         try:
#             payload = jwt.decode(token,settings.SECRET_KEY)
#             user = User.objects.get(id=payload['user_id'])
            
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.is_active = True
#                 user.save()
            
#                 return Response({
#                     'status':'success',
#                     'email': ' Successfully Activated'})
#             else:
#                 return Response({
#                     'status':'success',
#                     'email': ' Link is no longer valid'})
        
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Link  Expired'},status=status.HTTP_400_BAD_REQUEST)
        
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': ' Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        
            
    
class LoginAPIView(APIView):
    serializer_class = LoginSerializer  
    permission_classes= (AllowAny,)
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if  serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if  user.exists() and user[0].auth_provider :
                    if user.check_password(password):
                        if user.is_active :
                            if user.is_verified :
                                login(request, user)
                                refresh_token = RefreshToken.for_user(user)
                                access_token = refresh_token.access_token
                                # return Response({'status':'success',
                                #             'userInfo': serializer.data,
                                #              'refresh_token':refresh_token,
                                #              'access_token':access_token},status=status.HTTP_200_OK)
                                return Response({'status':'success',
                                                'userInfo':{
                                                    'username':user.username, 
                                                    'email':user.email,
                                                    'first_name':user.first_name,
                                                    'last_name':user.last_name,
                                                    'sex':user.sex
                                                    },
                                                'refresh_token':str(refresh_token),
                                                'access_token':str(access_token)},status=status.HTTP_200_OK)

                            else:
                                return Response({'status':'error',
                                                'message':'User not Verified'},status=status.HTTP_401_UNAUTHORIZED)
                        else:
                                return Response({'status':'error',
                                                'message':'User not Active'},status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({'status':'error',
                                        'message':'Incorrect Password'},status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'status':'error',
                                    'message':'Please  continue your login using +'},status=status.HTTP_401_UNAUTHORIZED)
            except:
                    return Response({'status':'error',
                                    'message':'User not found'},status=status.HTTP_400_BAD_REQUEST)
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
        
                

class InitiateForgotPasswordView(APIView):
    serializer_class = InitiateForgotPasswordSerializer
    permission_classes= (AllowAny,)
    
    @swagger_auto_schema(request_body=InitiateForgotPasswordSerializer)
    def post(self, request):
        serializer = InitiateForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user_data = serializer.data
            email= user_data['email']
            try:
                user = User.objects.get(email=email)
                
                keygen=generateKey()
                print('keygen:',keygen)
                key = base64.b32encode(keygen.returnValue(email).encode())
                OTP = pyotp.TOTP(key, interval= settings.OTP_TIMEOUT)
                print(str(OTP.now()))
                d_token= str(OTP.now())
                
                email_body = 'Hi '+ user.first_name  + ' ' + user.last_name +','+ '\n Use this OTP  to reset your account: ' + d_token + '\n Please note that the OTP expires in ' + str(int(settings.OTP_TIMEOUT/60)-1)+ ' minutes'
                data = {'email_body':email_body,'to_email':email,'email_subject':'Your Password Reset'}
                SendEmail.send_email(data)
                
                print('Mail Sent')
                
                return Response({'status':'success','code':d_token, 'message':'Check your mail for your reset OTP'},status=status.HTTP_200_OK)
            except:
                return Response({'status':'error','message':'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)        
            
            
class VerifyPasswordResetView(APIView):
    serializer_class = VerifyPasswordResetSerializer
    permission_classes= (AllowAny,)
    
    
    @swagger_auto_schema(request_body=VerifyPasswordResetSerializer)
    def post(self, request):
        serializer = VerifyPasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            
            try:
                email = serializer.data['email']
                code = serializer.data['code']
                user = User.objects.get(email=email)
                keygen=generateKey()
                print('keygen:',keygen)
                key = base64.b32encode(keygen.returnValue(email).encode())
                OTP = pyotp.TOTP(key, interval= settings.OTP_TIMEOUT)
                
                
                if OTP.verify(code):
                    login(request,user)
                    refresh_token=RefreshToken.for_user(user)
                    
                    return Response({
                        'status': 'success',
                        'message':'Reset Password OTP Verification Successful',
                        'refresh_token': str(refresh_token),
                        'access_token':str(refresh_token.access_token)
                        
                    },status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status':'error',
                        'message':' Invalid Code'
                        },status=status.HTTP_400_BAD_REQUEST)
            
            except:
                return Response({
                    'status':'error',
                    'message':' User not found'
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
            
class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        
        serializer= ResetPasswordSerializer
        if serializer.is_valid():
            password1= serializer.data['password']
            password2= serializer.data['confirm_password']
            user = User.objects.get(id=request.user.id)
            
            if password1 == password2:
                user.set_password(password1)
                user.save()
                return Response({
                    'status':'success',
                    'message':'User Password was successfully changed'
                },status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'status':'error',
                    'message':'Password Mismatch'
                },status=status.HTTP_400_BAD_REQUEST)
                
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)          
            
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user= request.user
            old_password = serializer.validated_data['old_password']
            
            if not user.check_password(old_password):
                return Response({
                    'status':'error',
                    'message':'Incorrect Password'
                },status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({
                'status':'success',
                'message':'Password changed successfully'
            },status=status.HTTP_200_OK)  
            
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
            
class LogoutView (APIView):
    
    def get (self,request):
        user= request.user
        
        logout(request)
        
        return Response({
            'status': 'success',
            'message':'Logout Success'
        },status=status.HTTP_200_OK)