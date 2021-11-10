from google.auth.transport import requests
from google.oauth2 import id_token



class Google:
    # This Google class is to fetch the user info and return it
    
    @staticmethod
    def validate(auth_token):
        
    # Validate Methond Queries the Google oauth2 api to fetch the user info
        
        try:
            idinfo = id_token.verify_oauth_token(auth_token,requests.Request())    
            
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        
        except:
            return 'The token is either invalid or has expired'
    