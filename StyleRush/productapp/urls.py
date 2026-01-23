from django.urls import path
from .views import edit_product, delete_product, delete_variant, add_variants, products_page, add_product
from .views import update_variant_image, update_variant_price, update_variant_stock, add_variant_from_edit

urlpatterns = [
    path('products/', products_page, name='products'),
    path('products/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('variant/<int:variant_id>/delete/', delete_variant, name='delete_variant'),
    path('add-product/', add_product, name='add_product'),
    path('add-variant/<int:product_id>/', add_variants, name='add_variants'),
    path('variant/<int:variant_id>/update-image/', update_variant_image, name='update_variant_image'),
    path('variant/<int:variant_id>/update-price/', update_variant_price, name='update_variant_price'),
    path('variant/<int:variant_id>/update-stock/', update_variant_stock, name='update_variant_stock'),
    path('product/<int:product_id>/add-variant/', add_variant_from_edit, name='add_variant_from_edit'),

]
