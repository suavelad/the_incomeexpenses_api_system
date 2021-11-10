from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager, PermissionsMixin)

from  .manager import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken



# Create your models here.

class User (AbstractBaseUser, PermissionsMixin):

    SEX = (
        ('male','Male'),
        ('female','Female')
    )

    AUTH_PROVIDERS = {'facebook':'facebook','google':'google','twitter':'twitter','email':'email'}

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField( max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    sex= models.CharField(max_length=255, choices=SEX, null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255,blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    objects = CustomUserManager()


    def __str__(self) -> str:
        return self.email

    
    def tokens (self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access': str(refresh.access_token)
        }
