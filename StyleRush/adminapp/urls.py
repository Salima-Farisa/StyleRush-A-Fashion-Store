from django.urls import path
from .views import login_admin, admin_logout, dashboard, orders_page, customers, profile_view, edit_profile, update_order_status, customer_detail

urlpatterns = [
    path('', login_admin, name="login_admin"),
    path('admin-logout/', admin_logout, name="admin_logout"),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='admin_profile'),
    path('profile/edit/', edit_profile, name='admin_edit_profile'),
    path('orders/', orders_page, name='orders'),
    path('orders/update/<int:order_id>/', update_order_status, name='update_order_status'),
    path('customers/', customers, name='customers'),
]
