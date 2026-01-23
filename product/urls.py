from django.urls import path
from .views import home, subscribe, product_list, product_detail, about, send_message, products_by_brand
from .views import profile_view, edit_profile

urlpatterns = [
    path('', home, name="home"),
    path('subscribe/', subscribe, name='subscribe'),
    path('about/', about, name="about"),
    path('brand/<int:brand_id>/', products_by_brand, name='products_by_brand'),
    path('products-list/', product_list, name="products_list"),
    path('products/category/<int:category_id>/', product_list, name='products_by_category'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('subscribe/', subscribe, name='subscribe'),
    path('send-message/', send_message, name='send_message'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

]