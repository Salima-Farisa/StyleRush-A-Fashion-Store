from django.urls import path
from .views import add_brand, add_category, add_color, add_size, categories, brands, colors, sizes
from .views import edit_category, delete_category, edit_brand, delete_brand, edit_color, delete_color, edit_size, delete_size

urlpatterns = [
    path('add-category/', add_category, name='add_category'),
    path('add-brand/', add_brand, name='add_brand'),
    path('add-color/', add_color, name='add_color'),
    path('add-size/', add_size, name='add_size'),
    path('categories/', categories, name="categories"),
    path('brands/', brands, name="brands"),
    path('colors/', colors, name="colors"),
    path('size/', sizes, name="size"),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    path('brands/edit/<int:brand_id>/', edit_brand, name='edit_brand'),
    path('brands/delete/<int:brand_id>/', delete_brand, name='delete_brand'),
    path('colors/edit/<int:color_id>/', edit_color, name='edit_color'),
    path('colors/delete/<int:color_id>/', delete_color, name='delete_color'),
    path('size/edit/<int:size_id>/', edit_size, name='edit_size'),
    path('size/delete/<int:size_id>/', delete_size, name='delete_size'),

]

