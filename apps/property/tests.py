import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from apps.landlords.models import Landlord
from apps.tenants.models import Tenant

from apps.users.models import UserAccount

from apps.property.models import Contract, Property



class PropertyTests(TestCase):

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

        self.landlord = Landlord.objects.create(user=self.landlord_user, contact_number='0123456789')
        # create an auth token for the test user
        self.token = Token.objects.create(user=self.landlord_user)
        # set the auth token for the test client
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
        # create property data
        self.property_data = {
            "landlord": self.landlord.id,
            "property_name": "Test Property 1",
            "type": "HOUSE",
            "description": "Test Description 1",
            "address": "Test Address 1",
            "status": "OPEN"
        }
        
        self.update_data = {
            'property_name': 'New Property Name',
            'type': 'APARTMENT',
            'description': 'New Description',
            'address': 'New Address',
            'status': 'BOOKED'
        }
    
        self.property_data_for_object = {
            "landlord": self.landlord,
            "property_name": "Test Property 1",
            "type": "HOUSE",
            "description": "Test Description 1",
            "address": "Test Address 1",
            "status": "OPEN"
        }

        self.property = Property.objects.create(
            landlord=self.property_data_for_object["landlord"],
            property_name=self.property_data_for_object["property_name"],
            type=self.property_data_for_object["type"],
            description=self.property_data_for_object["description"],
            address=self.property_data_for_object["address"],
            status=self.property_data_for_object["status"],
        )

    def test_create_property(self):

        url = reverse('property:property-list')
        data = self.property_data
        response = self.client.post(url, data=data)

        # get the created property
        property = Property.objects.get(landlord__id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(property)


    def test_delete_property(self):

        # create a property that we will delete
        url = reverse('property:property-list')
        data = self.property_data
        response = self.client.post(url, data=data)

        # get the property
        property = Property.objects.all()[0]
        property_dict = response.json()
        property_dict["id"] = property.id

        # did we successfully create the property
        self.assertTrue(property.id, 1)

        # delete the property
        url = reverse('property:property-detail', kwargs={'pk': property.id})
        response = self.client.delete(url)

        # try to get the property 
        property = Property.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(property), 2)  

    def test_update_invoice(self):
        
        # create a property that we will update
        url = reverse('property:property-list')
        data = self.property_data
        response = self.client.post(url, data=data)

        # get the invoice
        property = Property.objects.all()[0]
        property_dict = response.json()
        property_dict["id"] = property.id

        # prepare the url
        url = reverse('property:property-detail', kwargs={"pk":property_dict["id"]})

        # change the data
        property_dict["property"]["status"] = "BOOKED"
        property_json = json.dumps(property_dict["property"])

        # update the invoice with new data
        response = self.client.put(url, data=property_json, content_type='application/json')

        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(property_dict['property']['status'], response.json()['status'])  
        

class ContractTests(TestCase):

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

        landlord = Landlord.objects.create(user=self.landlord_user, contact_number='0123456789')
        tenant = Tenant.objects.create(user=self.tenant_user)
        
        # create an auth token for the test user
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

        


        # create test contract data
        self.contract_data = {
            "property": self.property.id,
            "tenant": tenant.id,
            "landlord":landlord,
            "contract_starts":"2022-01-01",
            "contract_ends":"2024-01-01",
            "payment_type":"MONTHLY",
            "rental_amount":"500.00",
            "contract_status":True
        }

        self.contract_data_for_object = {
            "property": self.property,
            "tenant": tenant,
            "landlord":landlord,
            "contract_starts":"2022-01-01",
            "contract_ends":"2023-01-01",
            "payment_type":"MONTHLY",
            "rental_amount":"500.00",
            "contract_status":True
        }

        self.contract = Contract.objects.create(
            property = self.contract_data_for_object["property"],
            tenant = self.contract_data_for_object["tenant"],
            landlord= self.contract_data_for_object["landlord"],
            contract_starts = self.contract_data_for_object["contract_starts"],
            contract_ends= self.contract_data_for_object["contract_ends"],
            payment_type= self.contract_data_for_object["payment_type"],
            rental_amount= self.contract_data_for_object["rental_amount"],
            contract_status= self.contract_data_for_object["contract_status"]
        )

    def test_create_contract(self): 
        url = reverse('property:contract-list')
        data = self.contract_data
        response = self.client.post(url, data=data)

        # get the created contract
        contract = Contract.objects.get(landlord__id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(contract)


    def test_delete_contract(self):

        # create a contract that we will delete
        url = reverse('property:contract-list')
        data = self.contract_data
        response = self.client.post(url, data=data)

        # get the contract
        contract = Contract.objects.all()[0]
        contract_dict = response.json()
        contract_dict["id"] = contract.id

        # did we successfully create the contract
        self.assertTrue(contract.id, 1)

        # delete the contract
        url = reverse('property:contract-detail', kwargs={'pk': contract.id})
        response = self.client.delete(url)

        # try to get the contract 
        contract = Contract.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(contract), 2)

    def test_update_contract(self):
        
        # create a contract that we will update
        url = reverse('property:contract-list')
        data = self.contract_data
        response = self.client.post(url, data=data)

        # get the contract
        contract = Contract.objects.all()[0]
        contract_dict = response.json()
        contract_dict["id"] = contract.id

        # prepare the url
        url = reverse('property:contract-detail', kwargs={"pk":contract_dict["id"]})

        # change the data
        contract_dict["contract"]["payment_type"] = "WEEKLY"
        contract_json = json.dumps(contract_dict["contract"])

        # update the invoice with new data
        response = self.client.put(url, data=contract_json, content_type='application/json')
        
        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(contract_dict['contract']['payment_type'], response.json()['payment_type'])   


    def test_list_invoices(self):
        response = self.client.get(reverse('property:contract-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)