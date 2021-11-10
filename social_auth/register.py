from django.contrib.auth.models import User
from decouple  import config
from django.contrib.auth import authenticate,login, logout
from rest_framework.exceptions import AuthenticationFailed
import random



def generate_username(name):
    username = ''.join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0,1000))
        return generate_username(random_username)
def register_social_user(provider, user, email,first_name,last_name):
    get_user = User.objects.filter(email=email)
    
    if get_user.exists():
        if provider == get_user.provider:
            get_user = authenticate(email=email, password= config('SOCIAL_KEY'))
            
            return {
                'username': get_user.username,
                'email': get_user.email,
                'first_name': get_user.first_name,
                'last_name': get_user.last_name,
                'sex': get_user.sex,
                'access_token': get_user.tokens()['access'],
                'refresh_token': get_user.tokens()['refresh']
            }
        else:
            raise AuthenticationFailed(
                details='Please continue your login using ' + get_user[0].auth_provider
            )
    else:
        user={
            'username': generate_username(first_name),
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        user = User.objects.create(**user)
        user.is_verified = True
        user.is_active = True
        user.auth_provider= provider
        user.save()
        
        new_user = authenticate(email=email, password= config('SOCIAL_KEY'))
        
        return {
            'username': new_user.username,
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'sex': new_user.sex,
            'access_token': get_user.tokens()['access'],
            'refresh_token': get_user.tokens()['refresh']
        }