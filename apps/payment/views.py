from django.shortcuts import render
from apps.payment.serializers import PaymentSerializer
from apps.payment.models import Payment
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PaymentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'Payment created successfully',
                             'data': serializer.data,
                             'status': status.HTTP_201_CREATED}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {'message': 'Payment creation failed',
                             'data': serializer.errors,
                             'status': status.HTTP_400_BAD_REQUEST}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class PaymentUpdateView(generics.UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated,]

    def put(self,request, *args, **kwargs):
        partial = kwargs.pop('patial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {'message': 'Payment updated successfully',
                         'data': serializer.data,
                         'status': status.HTTP_200_OK}
        return Response(response_data)

class PaymentDeleteView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated,]

    def delete(self, request, pk):
        try:
            instance = Payment.objects.get(pk=pk)
            self.check_object_permissions(request, instance)
            instance.delete()
            response_data = {'message': 'Payment deleted successfully',
                             'data': {},
                             'status': status.HTTP_204_NO_CONTENT}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Payment.DoesNotExist:
            response_data = {'message': 'Payment detail not found',
                             'data': {},
                             'status': status.HTTP_404_NOT_FOUND}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class PaymentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
