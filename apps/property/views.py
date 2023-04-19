from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.landlords.models import Landlord
from apps.property.models import Contract, Property
from apps.property.serializers import ContractSerializer, PropertySerializer
from apps.tenants.models import Tenant


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        # create the property
        property = PropertySerializer(data=request.data)
        if property.is_valid():
            property.save()

        response_data = {
            "status": 201,
            "message": "Property created successfully",
            "property": property.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):

        # ====================
        # update the property using the data provided by the user
        # ====================

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        user = self.request.user
        # Determine if the user is a landlord or tenant and filter the invoices accordingly
        if user.type == 'LANDLORD' or user.type == 'Landlord':
            # get the landlord
            queryset = Landlord.objects.filter(user=user)
        else:
            # get tenant
            tenant = Tenant.objects.get(user=user)
            queryset = Landlord.objects.filter(tenant=tenant)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer

    def create(self, request, *args, **kwargs):
        
        # ====================
        # create the contract using the data provided by the user
        # ====================

        # create the contract
        contract = ContractSerializer(data=request.data)
        if contract.is_valid():
            contract.save()

        response_data = {
            "status": 201,
            "message": "Contract created successfully",
            "contract": contract.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    

    def get_queryset(self):
        user = self.request.user
        # Determine if the user is a landlord or tenant and filter the invoices accordingly
        if user.type == 'LANDLORD' or user.type == 'Landlord':
            # get the landlord
            landlord = Landlord.objects.get(user=user)
            queryset = Contract.objects.filter(landlord_id=landlord.id)
        else:
            # get tenant
            tenant = Tenant.objects.get(user=user)
            queryset = Contract.objects.filter(tenant_id=tenant.id)
        return queryset

    def update(self, request, *args, **kwargs):

        # ====================
        # update the contract using the data provided by the user
        # ====================

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
