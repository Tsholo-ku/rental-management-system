from django.urls import path
from apps.property.views import PropertyListView, PropertyCreateView, PropertyUpdateView, PropertyDeleteView, Property_Detail, ContractListView, ContractCreateView, ContractDeleteView, ContractUpdateView, LinkedContractView

app_name = 'property'
urlpatterns = [
    path('', PropertyListView.as_view(), name='property-list'),
    path('add/', PropertyCreateView.as_view(), name='property-add'),
    path('update/<int:pk>/', PropertyUpdateView.as_view(), name='property-update'),
    path('delete/<int:pk>/', PropertyDeleteView.as_view(), name='property-delete'),
    path('detail/<int:pk>/', Property_Detail.as_view(), name='search_primary_key'),
    path('contract/add/', ContractCreateView.as_view(), name='property-add'),
    path('contract/update/<int:pk>/',
         ContractUpdateView.as_view(), name='property-update'),
    path('contract/delete/<int:pk>/',
         ContractDeleteView.as_view(), name='property-delete'),
    path('contract/list/', LinkedContractView.as_view(), name='linked-contract'),
]
