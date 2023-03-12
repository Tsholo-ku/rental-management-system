from rest_framework import (
    authentication, generics, permissions, status, viewsets)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.invoices.serializers import InvoiceSerializer

from apps.invoices.models import Invoice


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InvoiceCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = InvoiceSerializer

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'Invoice created successfully',
                             'data': serializer.data,
                             'status': status.HTTP_201_CREATED}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {'message': 'Invoice creation failed',
                             'data': serializer.errors,
                             'status': status.HTTP_400_BAD_REQUEST}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class InvoiceUpdateView(generics.UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {'message': 'Invoice updated successfully',
                         'data': serializer.data,
                         'status': status.HTTP_200_OK}
        return Response(response_data)


class InvoiceDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def delete(self, request, pk):
        try:
            instance = Invoice.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            response_data = {'message': 'Invoice deleted successfully',
                             'data': {},
                             'status': status.HTTP_204_NO_CONTENT}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            response_data = {'message': 'Invoice not found',
                             'data': {},
                             'status': status.HTTP_404_NOT_FOUND}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class InvoiceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
