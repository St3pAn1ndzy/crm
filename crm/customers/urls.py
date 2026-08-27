from django.urls import path

from .views import (
    CustomersListView,
    CustomerDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
    convert_lead_to_customer_view,
)

app_name = 'customers'

urlpatterns = [
    path('customers/', CustomersListView.as_view(), name='customers-list'),
    path('customers/new/', convert_lead_to_customer_view, name='customers-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customers-detail'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customers-update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customers-delete'),
]
