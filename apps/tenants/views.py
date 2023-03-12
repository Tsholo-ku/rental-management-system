from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, generics, status, authentication, permissions

from apps.tenants.serializers import TenantSerializer
from apps.tenants.models import Tenant
from apps.property.serializers import ContractSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from apps.landlords.models import PropertyOwner


class TenantListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TenantSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        owner_instance = PropertyOwner.objects.get(
            user=user)

        return Tenant.objects.filter(owner=owner_instance)


class TenantRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request, pk):
        try:
            owner_instance = PropertyOwner.objects.get(
                user=request.user)
            tenant_instance = Tenant.objects.get(pk=pk)
            tenant_instance.owner.remove(owner_instance)
            owner_instance.tenants.remove(tenant_instance)
            response_data = {'message': 'Tenant removed successfully',
                             'data': {},
                             'status': 200}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            response_data = {'message': 'Property not found',
                             'data': {},
                             'status': status.HTTP_404_NOT_FOUND}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)