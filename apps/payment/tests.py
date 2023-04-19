from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from apps.landlords.models import Landlord
from apps.payment.models import Payment
from apps.tenants.models import Tenant
from apps.property.models import Contract
import json

from apps.users.models import UserAccount
from apps.property.models import Property



class PaymentTests(TestCase):
    
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
        # Create a test contract
        self.contract_starts = '2022-01-01'
        self.contract_ends = '2023-01-01'
        self.rental_amount = 1000.00
        self.payment_type= 'MONTHLY'
        self.contract_status= True

        self.contract = Contract.objects.create(
            property = self.property,
            tenant = tenant,
            landlord= landlord,
            contract_starts = self.contract_starts,
            contract_ends= self.contract_ends,
            payment_type= self.payment_type,
            rental_amount= self.rental_amount,
            contract_status= self.contract_status
        )
        contract = Contract.objects.get(id=1)
        # create test contract data
        self.contract_data = {
            "property": self.property,
            "tenant": tenant,
            "landlord":landlord,
            "contract_starts":"2022-01-01",
            "contract_ends":"2023-01-01",
            "payment_type":"MONTHLY",
            "rental_amount":"500.00",
            "contract_status":True
        }
        # create test payment
        self.payment = Payment.objects.create(
            contract_id= contract,
            tenant_id = tenant,
            property_owner_id = landlord,
            payment_method ='CASH',
            payment_amount = '1000',
            payment_status =True
        )
        

      
  

    def test_create_payment(self):

        url = reverse('payment:payment-list')
        data = {
            "contract_id" : self.payment.contract_id,
            "tenant_id" : self.payment.tenant_id,
            "property_owner_id" : self.payment.property_owner_id,
            "payment_method" : self.payment.payment_method,
            "payment_amount" : self.payment.payment_amount,
            "payment_status" : self.payment.payment_status

        }
        response = self.client.post(url, data=data)

        # get the created payment
        payment = Payment.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(payment)
    
    def test_list_payment(self):
        response = self.client.get(reverse('payment:payment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_payment(self):
        
        # create an payment that we will update
        url = reverse('payment:payment-list')
        data = {
            "contract_id" : self.payment.contract_id,
            "tenant_id" : self.payment.tenant_id,
            "property_owner_id" : self.payment.property_owner_id,
            "payment_method" : self.payment.payment_method,
            "payment_amount" : self.payment.payment_amount,
            "payment_status" : self.payment.payment_status

        }
        response = self.client.post(url, data=data)

        # get the payment
        payment = Payment.objects.all()[0]
        payment_dict = response.json()
        payment_dict["id"] = payment.id

        # prepare the url
        url = reverse('payment:payment-detail', kwargs={"pk":payment_dict["id"]})

        # change the data
        payment_dict["landlord"]["payment_amount"] = 2000.0
        payment_json = json.dumps(payment_dict["landlord"])

        # update the payment with new data
        response = self.client.put(url, data=payment_json, content_type='application/json')

        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payment_dict['landlord']['payment_amount'], response.json()['payment_amount'])
        
    def test_delete_payment(self):
        Payment.objects.all().delete()
        # create an payment that we will delete
        url = reverse('payment:payment-list')
        data = {
            "contract_id" : self.payment.contract_id,
            "tenant_id" : self.payment.tenant_id,
            "property_owner_id" : self.payment.property_owner_id,
            "payment_method" : self.payment.payment_method,
            "payment_amount" : self.payment.payment_amount,
            "payment_status" : self.payment.payment_status

        }
        response = self.client.post(url, data=data)

        # get the payment
        payment = Payment.objects.all()[0]
        payment_dict = response.json()
        payment_dict["id"] = payment.id

        # did we successfully create the payment
        self.assertTrue(payment.id, 1)

        # delete the payment
        url = reverse('payment:payment-detail', kwargs={'pk': payment.id})
        response = self.client.delete(url)

        # try to get the payment 
        payment = Payment.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(payment), 1)
