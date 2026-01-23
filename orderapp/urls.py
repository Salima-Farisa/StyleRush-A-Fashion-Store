from django.urls import path
from .views import order_success, order_page, cancel_order, track_order, order_detail

urlpatterns = [
   path('order/success/<int:order_id>/', order_success, name='order_success'),
   path('', order_page, name='order_list'),
   path('cancel-order/<int:order_id>/', cancel_order, name='cancel_order'),
   path('track-order/<int:order_id>/', track_order, name='track_order'),
   path('details/<int:order_id>/',order_detail , name='order_detail'),

]



