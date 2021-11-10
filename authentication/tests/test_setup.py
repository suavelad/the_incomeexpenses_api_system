
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        
        self.fake = Faker()
        
        
        # self.user_data = {
        #     'email': 'user@example.com',
        #     'username': 'user',
        #     'password': 'user@example.com',
        #     'first_name': 'John',
        #     'last_name': 'Doe',
        #     'sex':'male'
        # }
        # self.user_login_data = {
        #     'email': 'user@example.com',
          
        #     'password': 'user@example.com'
            
        # }
        
        self.user_data = {
            'email': self.fake.email(),
            'username': self.fake.email().split('@')[0],
            'password': self.fake.email(),
            'first_name': self.fake.email().split('@')[0],
            'last_name': self.fake.email().split('@')[0],
            'sex':'male'
        }
        self.user_login_data = {
            'email': self.fake.email(),
          
            'password': self.fake.email()
            
        }
        
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()