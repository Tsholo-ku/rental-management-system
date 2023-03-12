from django.urls import path
from .views import PaymentCreateView, PaymentListView, PaymentUpdateView, PaymentDeleteView

app_name = 'payment'
urlpatterns = [
    path('',PaymentListView.as_view(), name='payment_list'),
    path('add/',PaymentCreateView.as_view(), name='payment_add'),
    path('update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('delete/<int:pk>/',PaymentDeleteView.as_view(), name= 'payment_delete'),
]
