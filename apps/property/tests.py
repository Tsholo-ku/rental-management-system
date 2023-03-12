from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from apps.users.models import UserAccount

from .models import Property
from .serializers import PropertySerializer


class PropertyTests(TestCase):

    def setUp(self):

        self.client = APIClient()
        # create a test user
        self.username = 'testuser'
        self.full_name = 'test user'
        self.email = 'testuser@example.com'
        self.password = 'testpass123'
        self.user = UserAccount.objects.create_user(
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password
        )
        # create an auth token for the test user
        self.token = Token.objects.create(user=self.user)
        # set the auth token for the test client
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)

        self.property1 = Property.objects.create(
            property_name='Test Property 1',
            type='HOUSE',
            description='Test Description 1',
            address='Test Address 1',
            status = 'BOOKED'
        )
        self.property2 = Property.objects.create(
            property_name='Test Property 2',
            type='APARTMENT',
            description='Test Description 2',
            address='Test Address 2',
            status = 'ON REVIEW'
        )

        self.valid_property_data = {
            "property_name": "Test Property 3",
            "type": "HOUSE",
            "description": "Test Description 3",
            "address": "Test Address 3",
            "status": "OPEN"
        }
        self.invalid_property_data = {
            "property_name": "",
            "type": "HOUSE",
            "description": "Test Description 3",
            "address": "Test Address 3",
            "status": "ON HOLD"
        }
        self.property = Property.objects.create(
            property_name='Test Property',
            type='HOUSE',
            description='Test Description',
            address='Test Address',
            status='OPEN', 
        )
        self.valid_update_data = {
            'property_name': 'New Property Name',
            'type': 'APARTMENT',
            'description': 'New Description',
            'address': 'New Address',
            'status': 'BOOKED'
        }
        self.invalid_update_data = {
            'property_name': '',
            'type': '',
            'description': '',
            'address': '',
            'status': ''
        }

    def test_get_all_properties(self):
        user = UserAccount.objects.get(id=1)
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('property-list'))
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(response.content, JSONRenderer().render(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_valid_property(self):
        user = UserAccount.objects.get(id=1)
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        
        self.client = APIClient()
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.token = Token.objects.get_or_create(user=user)
        response = self.client.post(
            reverse('property-add'),
            data=self.valid_property_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       

    def test_create_invalid_property(self):
        self.client = APIClient()
        user = UserAccount.objects.get(id=1)
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            reverse('property-add'),
            data=self.invalid_property_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_property(self):
        user = UserAccount.objects.get(id=1)
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)    
        response = self.client.patch(reverse('property-update', kwargs={'pk': self.property.id}),
        data=JSONRenderer().render(self.valid_update_data), # JSONRenderer, so we don't have to manually convert the payload to json, it will handle it for us
        content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_property(self):
        response = self.client.patch(reverse('property-update', kwargs={'pk': self.property.id}),
        data=JSONRenderer().render(self.invalid_update_data),
        content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # sending a delete request and checking to see if it's valid or not
    def test_invalid_delete_property(self):
        response = self.client.delete(reverse('property-delete', kwargs={'pk': 30}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_property(self):
        response = self.client.delete(reverse('property-delete', kwargs={'pk': self.property.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    



    def test_list_properties(self):
        self.client = APIClient()
        user = UserAccount.objects.get(id=1)
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # set the accept header to JSON
        self.client.accept = 'application/json'
        # make a GET request to the property list endpoint
        # get API response
        response = self.client.get(reverse('property-list'))

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the response data matches the serialized property objects
        # get data from db
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(response.content, JSONRenderer().render(serializer.data))
        
        