from django.contrib.auth.models import User
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,VerifyEmailView,LoginAPIView,InitiateForgotPasswordView,\
    VerifyPasswordResetView,RegisterUserView,ResetPasswordView,ChangePasswordView,LogoutView

router = DefaultRouter()


router.register('user',UserViewSet, 'user')

urlpatterns = router.urls
urlpatterns += [
    path('login/',LoginAPIView.as_view(), name ='login'),
    path('logout',LogoutView.as_view(), name ='logout'),
    path('email-verify/',VerifyEmailView.as_view(), name ='email-verify'),
    path('refresh-token/',TokenRefreshView.as_view(), name ='refresh-token'),
    path('initiate-password-reset/',InitiateForgotPasswordView.as_view(), name ='initiate-password-reset'),
    path('verify-password-reset/',VerifyPasswordResetView.as_view(), name='verify-password-reset'),
    path('reset-password/',ResetPasswordView.as_view(), name='reset-password'),
    path('register/user/',RegisterUserView.as_view(), name='register'),
    path('change-password/',ChangePasswordView.as_view(), name='change-password'),
    
]
