"""
URL configuration for StyleRush project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# handler404='product.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),              # Default Django admin
    path('adminapp/', include('adminapp.urls')),

    # Login/logout only
    path('auth/', include('fashion.urls')),   

    # Product pages (home page also here)
    path('', include('product.urls')),

    # Cart
    path('cart/', include('cartapp.urls')),

   
    # Checkout
    path('checkout/', include('checkoutapp.urls')),

    # Orders
    path('order/', include('orderapp.urls')),

    # Wishlist
    path('wishlist/', include('wishlistapp.urls')),

    #productapp admin 
    path('productapp/', include('productapp.urls')),

    #productvariantapp admin 
    path('product-variant/', include('productvariantapp.urls')),

    #discountapp
    path('discount/', include('discountapp.urls')),

    #invoiceapp
    path('invoice/', include('invoice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

