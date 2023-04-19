import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.landlords.models import Landlord
from apps.property.models import Property
from apps.tenants.models import Tenant
from apps.users.models import UserAccount


class TenantTests(TestCase):
    
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

        self.landlord = Landlord.objects.create(user=self.landlord_user, contact_number='1234567890')
        self.tenant = Tenant.objects.create(user=self.tenant_user, address='123 Tenant Street')

        # create an auth token for the test tenant user
        self.token = Token.objects.create(user=self.tenant_user)

        # set the auth token for the test client
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create test property
        self.property = Property.objects.create(
            property_name='Test Property',
            type='HOUSE',
            description='Test Description',
            address='Test Address',
            status='OPEN',
            landlord=self.landlord
        ) 
  
        self.tenant_data = {
            "user": self.tenant_user.id,
            "address": self.tenant_address,
            "property": self.property.id
        }

    def test_create_tenant(self):

        url = reverse('tenants:tenant-list')
        data = {
            "user" : self.tenant_user,
            "address" : self.tenant_address,
            "property": self.property

        }
        response = self.client.post(url, data=data)

        # get the created tenant
        tenant = Tenant.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(tenant)
    
    def test_list_tenant(self):
        response = self.client.get(reverse('tenants:tenant-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_tenant(self):
        
        # create a tenant that we will update
        url = reverse('tenants:tenant-list')
        data = {
            "user" : self.tenant_user,
            "address" : self.tenant_address,
            "property": self.property,
            "landlord": self.landlord
        }
        response = self.client.post(url, data=data)

        # get the tenant
        tenant = Tenant.objects.all()[0]
        tenant_dict = response.json()
        tenant_dict["id"] = tenant.id

        # prepare the url
        url = reverse('tenants:tenant-detail', kwargs={"pk":tenant_dict["id"]})

        # change the data
        tenant_dict["tenant"]["address"] = "123 Tenant Street"
        tenant_json = json.dumps(tenant_dict["tenant"])

        # update the landlord with new data
        response = self.client.put(url, data=tenant_json, content_type='application/json')
        
        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tenant_dict['tenant']['address'], response.json()['address'])
        
    def test_delete_tenant(self):

        # create an tenant that we will delete
        url = reverse('tenants:tenant-list')
        data =  {
            "user" : self.tenant_user,
            "address" : self.tenant_address,
            "property": self.property,
            "landlord": self.landlord
        }
        response = self.client.post(url, data=data)

        # get the tenant
        tenant = Tenant.objects.all()[0]
        tenant_dict = response.json()
        tenant_dict["tenant"]["id"] = tenant.id

        # did we successfully create the tenant
        self.assertTrue(tenant.id, 1)

        # delete the tenant
        url = reverse('tenants:tenant-detail', kwargs={'pk': tenant.id})
        response = self.client.delete(url)

        # try to get the tenant 
        tenant = Tenant.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(tenant), 1)
