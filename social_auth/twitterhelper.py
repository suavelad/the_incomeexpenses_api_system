
from decouple import config

from rest_framework import serializers
import twitter



class TwitterAuthTokenVerification:
    
    
    """
    Class to  decode user access_token and user access_token_secret 
    tokens will combine the user access_token and user access_token_secret
    separated by space
    """
    
    
    @staticmethod
    def validate_twitter_auth_token(access_token_key, access_token_secret):
        
        """
        validate_twitter_auth_token methods returns a twitter user profile info
        """
        
        consumer_api_key =  config('TWITTER_API_KEY')
        consumer_api_secret = config('TWITTER_API_SECRET')
        
        try:
            api = twitter.Api(consumer_key = consumer_api_key, 
                              consumer_secret = consumer_api_secret,
                              access_token_key = access_token_key, 
                              access_token_secret=access_token_secret
                              )
            user_profile_info = api.VerifyCredentials(include_email=True)
            return user_profile_info.__dict__
        except: 
            raise serializers.ValidationError ({
                'tokens': ['The tokens are invalid or expired']
            })
            