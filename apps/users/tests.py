from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class RegistrationTestCase(APITestCase):
    def test_registration(self):
        #POST request to the registration API endpoint with the user's email, password, and full name as data.
        data = {'email': 'testuser@example.com', 'password': 'testpassword', 'full_name': 'Test User', 'username': 'testuser', 'type': 'LANDLORD'}
        response = self.client.post('/register/', data)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Registration successful')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #Checking the response status code to make sure it's 201 (CREATED)

        #To check if the user is created or not
        User = get_user_model()
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])

class LoginTestCase(APITestCase):

    def test_login(self):
        User.objects.create_user(username="admin",password="1234",email = "test@admin.com", full_name = "admin")
        data = {
            "username":"admin",
            "password":"1234"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)