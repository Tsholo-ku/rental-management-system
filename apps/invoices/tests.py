from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from apps.users.models import UserAccount
from apps.property.models import Property

from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceTests(TestCase):
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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # create test property
        self.property = Property.objects.create(
            property_name='Test Property',
            type='HOUSE',
            description='Test Description',
            address='Test Address',
            status='OPEN',
            owner=self.user
        )

        # create test invoice data
        self.valid_invoice_data = {
            "property_id": self.property.id,
            "invoice_number": "INV-1234",
            "date": "2022-01-01",
            "due_date": "2022-02-01",
            "amount": "1000.00",
            "status": "PENDING"
        }

        self.invalid_invoice_data = {
            "property_id": self.property.id,
            "invoice_number": "",
            "date": "2022-01-01",
            "due_date": "2022-02-01",
            "amount": "1000.00",
            "status": "PENDING"
        }

        # create test invoice
        self.invoice = Invoice.objects.create(
            property=self.property,
            invoice_number='INV-5678',
            date='2022-01-15',
            due_date='2022-02-15',
            amount='500.00',
            status='PAID'
        )

        # create test update data
        self.valid_update_data = {
            'property_id': self.property.id,
            'invoice_number': 'INV-5679',
            'date': '2022-01-20',
            'due_date': '2022-02-20',
            'amount': '750.00',
            'status': 'PENDING'
        }

        self.invalid_update_data = {
            'property_id': self.property.id,
            'invoice_number': '',
            'date': '2022-01-20',
            'due_date': '2022-02-20',
            'amount': '750.00',
            'status': 'PENDING'
        }

def test_get_all_invoices(self):
    response = self.client.get(reverse('invoice-list'))
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    self.assertEqual(response.content, JSONRenderer().render(serializer.data))
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_create_valid_invoice(self):
    response = self.client.post(
        reverse('invoice-add'),
        data=self.valid_invoice_data
    )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

def test_create_invalid_invoice(self):
    response = self.client.post(
        reverse('invoice-add'),
        data=self.invalid_invoice_data,
    content_type='application/json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_get_invoice_by_id(self):
    response = self.client.get(reverse('invoice-detail', args=[self.invoice.id]))
    invoice = Invoice.objects.get(id=self.invoice.id)
    serializer = InvoiceSerializer(invoice)
    self.assertEqual(response.content, JSONRenderer().render(serializer.data))
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_update_valid_invoice(self):
    response = self.client.put(
    reverse('invoice-detail', args=[self.invoice.id]),
    data=self.valid_update_data,
    content_type='application/json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_update_invalid_invoice(self):
    response = self.client.put(
    reverse('invoice-detail', args=[self.invoice.id]),
    data=self.invalid_update_data,
    content_type='application/json'
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_delete_invoice(self):
    response = self.client.delete(reverse('invoice-detail', args=[self.invoice.id]))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
