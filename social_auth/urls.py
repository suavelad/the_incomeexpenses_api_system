from django.contrib.auth.models import User
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()


# router.register('user',UserViewSet, 'user')

urlpatterns = router.urls
urlpatterns += [
    path('google/',GoogleSocialAuthView.as_view(), name ='google'),
    path('facebook/',FacebookSocialAuthView.as_view(), name ='facebook'),
    path('twitter/',TwitterSocialAuthView.as_view(), name ='twitter'),
    
]