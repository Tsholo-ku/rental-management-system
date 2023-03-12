from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import UserAccount
from apps.landlords.models import PropertyOwner
from apps.tenants.models import Tenant

from apps.users.serializers import LoginSerializer, UserSerializer

User = get_user_model()

# ViewSets define the view behavior.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# To register the user


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data, context={
                                    'request': self.request})

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data.get("password"))
        user.save()

        # create a PropertyOwner object if the user type is "LANDLORD"
        if serializer.validated_data['type'] == UserAccount.Types.LANDLORD:
            contact_number = serializer.validated_data.get('contact_number')
            property_owner = PropertyOwner.objects.create(
                user=user,
                contact_number=contact_number
            )
            property_owner.save()
            return Response({'message': 'Registration successful', 'status': 'success'}, status=status.HTTP_201_CREATED)

        elif serializer.validated_data['type'] == UserAccount.Types.TENANT:
            address = serializer.validated_data.get('address')
            tenant = Tenant.objects.create(
                user=user,
                address=address
            )
            tenant.save()
            return Response({'message': 'Registration successful', 'status': 'success'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': 'Registration failed', 'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={
                                     'request': self.request})  # initializes the serializer object
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        if user.type == 'LANDLORD':
            try:
                user_instance = PropertyOwner.objects.filter(
                    user=user).values('id')
                user_type_id = user_instance[0].get('id')
            except Exception as e:
                user_type_id = None

        if user.type == 'TENANT':
            try:
                user_instance = Tenant.objects.filter(user=user).values('id')
                user_type_id = user_instance[0].get('id')
            except Exception as e:
                user_type_id = None

        msg = {
            "message": "Login successful",
            "data": {
                "id": user.id,
                "username": user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_type': user.type,
                'user_type_id': user_type_id
            },
            "status": "Success"

        }
        return Response(msg, status=status.HTTP_200_OK)