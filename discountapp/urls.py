from django.urls import path
from .views import discount_list, add_discount, edit_discount, delete_discount

urlpatterns = [
    path('discounts/', discount_list, name='discount_list'),
    path('discount/add/<int:variant_id>/', add_discount, name='add_discount'),
    path('discount/edit/<int:discount_id>/', edit_discount, name='edit_discount'),
    path('discount/delete/<int:discount_id>/', delete_discount, name='delete_discount'),
]