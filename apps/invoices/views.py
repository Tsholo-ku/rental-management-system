from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.tenants.models import Tenant
from apps.landlords.models import Landlord

from apps.invoices.serializers import InvoiceSerializer

from apps.invoices.models import Invoice


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        # ====================
        # create the invoice using the data provided by the user
        # ====================
        response_status = status.HTTP_201_CREATED
        # create the invoice
        invoice = InvoiceSerializer(data=request.data)
        if invoice.is_valid():
            invoice.save()

            response_data = {
                "status": 201,
                "message": "Invoice created successfully",
                "invoice": invoice.data
            }

        else:
            response_status = status.HTTP_406_NOT_ACCEPTABLE
            response_data ={
                "status": 406,
                "message": "invalid invoice data"
            }

        return Response(response_data, status=response_status)

    def update(self, request, *args, **kwargs):

        # ====================
        # update the invoice using the data provided by the user
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
            landlord = Landlord.objects.get(user=user)
            queryset = Invoice.objects.filter(landlord=landlord)
        else:
            # get tenant
            tenant = Tenant.objects.get(user=user)
            queryset = Invoice.objects.filter(tenant=tenant)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
