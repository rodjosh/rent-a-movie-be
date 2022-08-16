from random import randint, random
from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {
            "username": f"randomuser",
            "email": f"randomuser@gmail.com",
            "password": "testpassword",
            "password2": "testpassword"
        }
        response = self.client.post('/user/register/', data)
        print(response)
        self.assertEqual(response.status_code, 200)
