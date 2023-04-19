from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from apps.landlords.models import Landlord
from apps.tenants.models import Tenant
import json

from apps.users.models import UserAccount
from apps.property.models import Property



class LandlordTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        # create a test landlord user
        self.landlord_username = 'testlandlord'
        self.landlord_full_name = 'test landlord'
        self.landlord_email = 'testlandlord@example.com'
        self.landlord_password = 'testpass123'
        self.landlord_contact_number = '0123456789'
        self.landlord_address = '123 Test Street'
        self.landlord_type = 'Landlord'
        self.landlord_user = UserAccount.objects.create_user(
            username=self.landlord_username,
            full_name=self.landlord_full_name,
            email=self.landlord_email,
            password=self.landlord_password,
            type=self.landlord_type
        )

        # create a test tenant user
        self.tenant_username = 'testtenant'
        self.tenant_full_name = 'test tenant'
        self.tenant_email = 'testtenant@example.com'
        self.tenant_password = 'testpass123'
        self.tenant_address = '123 Test Street'
        self.tenant_type = 'Tenant'
        self.tenant_user = UserAccount.objects.create_user(
            username=self.tenant_username,
            full_name=self.tenant_full_name,
            email=self.tenant_email,
            password=self.tenant_password,
            type=self.tenant_type
        )

        landlord = Landlord.objects.create(user=self.landlord_user, contact_number='1234567890')
        tenant = Tenant.objects.create(user=self.tenant_user)

        # create an auth token for the test landlord user
        self.token = Token.objects.create(user=self.landlord_user)

        # set the auth token for the test client
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create test property
        self.property = Property.objects.create(
            property_name='Test Property',
            type='HOUSE',
            description='Test Description',
            address='Test Address',
            status='OPEN',
            landlord=landlord
        )

   

      
  

    def test_create_Landlord(self):

        url = reverse('landlords:landlord-list')
        data = {
            "user" : self.landlord_user,
            "contact_number" : self.landlord_contact_number

        }
        response = self.client.post(url, data=data)

        # get the created landlord
        landlord = Landlord.objects.get(landlord=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(landlord)
    
    def test_list_landlord(self):
        response = self.client.get(reverse('landlords:landlord-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_landlord(self):
        
        # create an landlord that we will update
        url = reverse('landlords:landlord-list')
        data = {
            "user" : self.landlord_user,
            "contact_number" : self.landlord_contact_number

        }
        response = self.client.post(url, data=data)

        # get the landlord
        landlord = Landlord.objects.all()[0]
        landlord_dict = response.json()
        landlord_dict["landlord"]["id"] = landlord.id

        # prepare the url
        url = reverse('landlords:landlord-detail', kwargs={"pk":landlord_dict["landlord"]["id"]})

        # change the data
        landlord_dict["landlord"]["contact_number"] = "7489887864"
        landlord_json = json.dumps(landlord_dict["landlord"])

        # update the landlord with new data
        response = self.client.put(url, data=landlord_json, content_type='application/json')

        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(landlord_dict['landlord']['contact_number'], response.json()['contact_number'])
        
    def test_delete_landlord(self):

        # create an landlord that we will delete
        url = reverse('landlords:landlord-list')
        data = {
            "user" : self.landlord_user,
            "contact_number" : self.landlord_contact_number

        }
        response = self.client.post(url, data=data)

        # get the landlord
        landlord = Landlord.objects.all()[0]
        landlord_dict = response.json()
        landlord_dict["landlord"]["id"] = landlord.id

        # did we successfully create the landlord
        self.assertTrue(landlord.id, 1)

        # delete the landlord
        url = reverse('landlords:landlord-detail', kwargs={'pk': landlord.id})
        response = self.client.delete(url)

        # try to get the landlord 
        landlord = Landlord.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(landlord), 1)