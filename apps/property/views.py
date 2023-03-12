
from apps.property.serializers import PropertySerializer
from apps.property.models import Property
from rest_framework import viewsets, generics, status, authentication, permissions
from apps.property.models import Contract
from apps.property.serializers import ContractSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from apps.landlords.models import PropertyOwner
from apps.tenants.models import Tenant


class PropertyCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PropertySerializer

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        owner_instance = PropertyOwner.objects.get(user=request.user)
        if serializer.is_valid():
            instance = serializer.save()
            instance.owner = owner_instance
            instance.save()
            owner_instance.property.add(instance)

            response_data = {'message': 'Property created successfully',
                             'data': serializer.data,
                             'status': status.HTTP_201_CREATED}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {'message': 'Property creation failed',
                             'data': serializer.errors,
                             'status': status.HTTP_400_BAD_REQUEST}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated,]

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {'message': 'Property updated successfully',
                         'data': serializer.data,
                         'status': status.HTTP_200_OK}
        return Response(response_data)


class PropertyDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request, pk):
        try:
            instance = Property.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            response_data = {'message': 'Property deleted successfully',
                             'data': {},
                             'status': status.HTTP_204_NO_CONTENT}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist:
            response_data = {'message': 'Property not found',
                             'data': {},
                             'status': status.HTTP_404_NOT_FOUND}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class PropertyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PropertySerializer

    def get_queryset(self):
        user = self.request.user
        owner_instance = PropertyOwner.objects.get(
            user=user)

        return Property.objects.filter(owner=owner_instance)


class Property_Detail(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, pk):
        try:
            instance = Property.objects.get(pk=pk)
            serializer = PropertySerializer(instance)
            response_data = {'message': 'Record found',
                             'data': serializer.data,
                             'status': "SUCCESS"}
            return Response(response_data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            response_data = {'message': 'No record found',
                             'data': {},
                             'status': "FAILED"}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class ContractCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer

    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'Contract created successfully',
                             'data': serializer.data,
                             'status': "SUCCESS"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {'message': 'Contract creation failed',
                             'data': serializer.errors,
                             'status': status.HTTP_400_BAD_REQUEST}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ContractUpdateView(generics.UpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated,]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {'message': 'Contract updated successfully',
                         'data': serializer.data,
                         'status': status.HTTP_200_OK}
        return Response(response_data)


class ContractDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request, pk):
        try:
            instance = Contract.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            response_data = {'message': 'Contract deleted successfully',
                             'data': {},
                             'status': status.HTTP_204_NO_CONTENT}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Contract.DoesNotExist:
            response_data = {'message': 'Contract not found',
                             'data': {},
                             'status': status.HTTP_404_NOT_FOUND}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class ContractListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class LinkedContractView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ContractSerializer

    def get_queryset(self):
        user = self.request.user
        if user.type == 'LANDLORD':
            owner_instance = PropertyOwner.objects.get(user=user)
            return Contract.objects.filter(owner=owner_instance)
        elif user.type == 'TENANT':
            tenant_instance = Tenant.objects.get(user=user)
            return Contract.objects.filter(tenant=tenant_instance)
        else:
            data = {
                'message': 'User is not authenticated',
                'satus': status.HTTP_403_FORBIDDEN
            }
            raise AuthenticationFailed({'detail': data})
