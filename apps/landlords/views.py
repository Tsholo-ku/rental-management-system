from django.shortcuts import render
from rest_framework import generics, status
from apps.landlords.models import PropertyOwner
from apps.landlords.serializers import PropertyOwnerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.tenants.models import Tenant
from django.core.exceptions import ObjectDoesNotExist


class OwnerTenantList(generics.ListAPIView):
    serializer_class = PropertyOwnerSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = []
        try:
            tenant_list = PropertyOwner.objects.filter(
                user=request.user).values('tenants')
            if len(tenant_list) == 1 and tenant_list[0].get('tenants') == None:
                tenants = Tenant.objects.all().values_list(
                    'id', 'user__username')
                for tenant_instance in tenants:
                    data.append(
                        {'id': tenant_instance[0], 'tenant_name': tenant_instance[1]})

                response_data = {
                    'message': 'Tenants to add for the user',
                    'data': data,
                    'status': "SUCCESS"
                }
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                tenants = Tenant.objects.all().exclude(
                    id__in=[tenant.get('tenants') for tenant in tenant_list]).values_list(
                    'id', 'user__username')
                for tenant_instance in tenants:
                    data.append(
                        {'id': tenant_instance[0], 'tenant_name': tenant_instance[1]})

                response_data = {
                    'message': 'Tenants to add for the user',
                    'data': data,
                    'status': "SUCCESS"
                }
                return Response(response_data, status=status.HTTP_200_OK)

                pass

        except ObjectDoesNotExist:
            response_data = {
                'message': 'No tenants for the user',
                'data': [],
                'status': "SUCCESS"
            }
            return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.type != 'LANDLORD':
            response_data = {
                'message': 'User not eligible for adding tenant',
                'data': [],
                'status': "FAILED"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        tenant_id = request.data.get('id', None)
        if tenant_id:
            owner_instance = PropertyOwner.objects.get(user=request.user)
            try:
                tenant_instance = Tenant.objects.get(pk=tenant_id)
                tenant_instance.owner.add(owner_instance)
                owner_instance.tenants.add(tenant_instance)
                response_data = {
                    'message': 'Tenants added',
                    'data': [],
                    'status': "SUCCESS"
                }
                return Response(response_data, status=status.HTTP_200_OK)

                print(owner_instance)
            except Exception as e:
                print(str(e))
                response_data = {
                    'message': 'Failed adding tenant',
                    'data': [],
                    'status': "FAILED"
                }
                return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            'message': 'Please provide tenant',
            'data': [],
            'status': "FAILED"
        }
        return Response(response_data, status=400)
