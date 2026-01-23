from django.urls import path
from .views import select_address, billing_page, add_address, delete_address

urlpatterns = [
    path('', select_address, name='checkout'),
    path('checkout/add-address/', add_address, name='add_address'),
    path('delete-address/<int:address_id>/', delete_address, name='delete_address'),
    path('checkout/billing/', billing_page, name='billing_page'),

]
