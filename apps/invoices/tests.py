from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient
from apps.landlords.models import Landlord

from apps.property.models import Contract
from apps.tenants.models import Tenant
import json

from apps.users.models import UserAccount
from apps.property.models import Property

from apps.invoices.models import Invoice


class InvoiceTests(TestCase):
    
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

        # create/update test invoice data
        self.invoice_data = {
            "landlord": landlord.id,
            "tenant": tenant.id,
            "invoice_number": "INV-1234",
            "contract_id": contract.id,
            "invoice_amount": "1000.00",
            "notification_status": "ON REVIEW",
            "invoice_status": True
        }

        self.invoice_data_for_object = {
            "landlord": landlord,
            "tenant": tenant,
            "invoice_number": "INV-1234",
            "contract_id": contract,
            "invoice_amount": "1000.00",
            "notification_status": "ON REVIEW",
            "invoice_status": True
        }

        self.invoice = Invoice.objects.create(
            landlord=self.invoice_data_for_object["landlord"],
            tenant=self.invoice_data_for_object["tenant"],
            invoice_number=self.invoice_data_for_object["invoice_number"],
            contract_id=self.invoice_data_for_object["contract_id"],
            invoice_amount=self.invoice_data_for_object["invoice_amount"],
            notification_status=self.invoice_data_for_object["notification_status"],
        )

    def test_create_invoice(self):

        url = reverse('invoices:invoice-list')
        data = self.invoice_data
        response = self.client.post(url, data=data)

        # get the created invoice
        invoice = Invoice.objects.get(tenant__id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(invoice)
        self.assertTrue(invoice.invoice_status)
    
    def test_list_invoices(self):
        response = self.client.get(reverse('invoices:invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice(self):
        
        # create an invoice that we will update
        url = reverse('invoices:invoice-list')
        data = self.invoice_data
        response = self.client.post(url, data=data)

        # get the invoice
        invoice = Invoice.objects.all()[0]
        invoice_dict = response.json()
        invoice_dict["id"] = invoice.id

        # prepare the url
        url = reverse('invoices:invoice-detail', kwargs={"pk":invoice_dict["id"]})

        # change the data
        invoice_dict["invoice"]["notification_status"] = "PAID"
        invoice_json = json.dumps(invoice_dict["invoice"])

        # update the invoice with new data
        response = self.client.put(url, data=invoice_json, content_type='application/json')

        # test checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(invoice_dict['invoice']['notification_status'], response.json()['notification_status'])
        
    def test_delete_invoice(self):

        # create an invoice that we will update
        url = reverse('invoices:invoice-list')
        data = self.invoice_data
        response = self.client.post(url, data=data)

        # get the invoice
        invoice = Invoice.objects.all()[0]
        invoice_dict = response.json()
        invoice_dict["id"] = invoice.id

        # did we successfully create the invoice
        self.assertTrue(invoice.id, 1)

        # delete the invoice
        url = reverse('invoices:invoice-detail', kwargs={'pk': invoice.id})
        response = self.client.delete(url)

        # try to get the invoice 
        invoices = Invoice.objects.filter()

        # test checks
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(len(invoices), 1)