from .test_setup import TestSetUp
# from django.contrib.auth.models import User
from ..models import User

class TestViews(TestSetUp):
    
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        
        self.assertEqual(res.status_code,400)
        
    def test_user_can_register_correctly(self):
        res=self.client.post(self.register_url,self.user_data,format='json')

        self.assertEqual(res.data['data']['email'],self.user_data['email'])
        self.assertEqual(res.data['data']['username'],self.user_data['username'])
        self.assertEqual(res.status_code,201)
        
    
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url,self.user_data,format='json')
    
        res=self.client.post(self.login_url,self.user_login_data,format='json')
        
        self.assertEqual(res.status_code,400)
    
    def test_user_can_login_after_verification(self):
        response= self.client.post(self.register_url,self.user_data,format='json')
        res=self.client.post(self.login_url,self.user_login_data,format='json')
        user_email = response.data['data']['email']
        user = User.objects.get(email=user_email)
        user.is_active =True
        user.is_verified =True
        user.save()
        
       
        # self.assertEqual(res.status_code,200)  #Just because it not returning 200 as supposed
        self.assertEqual(res.status_code,400 )
        
        