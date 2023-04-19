from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from apps.landlords.models import Landlord
from apps.tenants.models import Tenant
from apps.users.models import UserAccount

User = get_user_model()

class RegistrationTestCase(APITestCase):
        
    def setUp(self):

        self.client = APIClient()
   

    def test_register_user(self):
        url = reverse('register')
        data = {"email": "testuser@example.com", 
                "password": "testpassword", 
                "full_name": "Test User", 
                "username": "testuser", 
                "type": "LANDLORD"
                }
        response = self.client.post(url, data=data)

        # get the created user
        user = UserAccount.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user)


class LoginTestCase(APITestCase):

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

       

    def test_login(self):

        url = reverse("token_obtain_pair")
        data = {
                "username": "testlandlord",
                "password": "testpass123"
            }
        response = self.client.post(url, data)
        self.token = response.data["access"]

        self.assertIsNotNone(self.token)


class LandlordFlowTests(TestCase):

    def setUp(self):

        # =========================
        # # create defaults
        # =========================

        # landlord
        landlorddata = {'email': 'landlorduser@example.com', 'password': 'landlordpassword', 'full_name': 'landlord User', 'username': 'landlorduser', 'type': 'LANDLORD'}
        reg_landlord = self.client.post('/register/', landlorddata)
        self.landlord = Landlord.objects.get(user__email=landlorddata["email"])

        # set this user as active
        self.user = self.landlord.user
        self.user.is_active = True
        self.user.save()

        # tenant
        tenantdata = {'email': 'tenantuser@example.com', 'password': 'tenantpassword', 'full_name': 'tenant User', 'username': 'tenantuser', 'type': 'TENANT'}
        reg_tenant = self.client.post('/register/', tenantdata)
        self.tenant = Tenant.objects.get(user__email=tenantdata["email"])

        # login 
        url = reverse("token_obtain_pair")
        data = {
            "username": "landlorduser",
            "password": "landlordpassword"
        }
        response = self.client.post(url, data)
        self.token = response.data["access"]


    def test_landlord_dashboard_page(self):

        # =========================
        # # simulate dashboard page
        # =========================

        # register a property +++
        data = {
            "property_name": "My property 1",
            "type": "APARTMENT",
            "description": "8 unit luxury apartment",
            "address": "12 downtheroad street, somewhere, 1203",
            "status": "OPEN",
        }
        url = reverse("property:property-list")
        response = self.client.post(
            url, 
            data, 
            HTTP_AUTHORIZATION="Bearer " + self.token,
        )

        pass
