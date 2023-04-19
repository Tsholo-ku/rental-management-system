from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.payment.models import Payment
from apps.payment.serializers import PaymentSerializer
from apps.tenants.models import Tenant


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        # ====================
        # create the landlord using the data provided by the user
        # ====================

        # create the invoice
        payment = PaymentSerializer(data=request.data)
        if payment.is_valid():
            payment.save()

        response_data = {
            "status": 201,
            "message": "Payment created successfully",
            "landlord": payment.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):

        # ====================
        # update the payment using the data provided by the user
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
            queryset = Payment.objects.filter(property_owner_id = user.id)
        else:
            # get tenant
            tenant = Tenant.objects.get(user=user)
            queryset = Payment.objects.filter(tenant_id=user.id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
