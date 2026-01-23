from django.urls import path
from .views import invoice_pdf

urlpatterns = [
    path('invoice/<int:invoice_id>/', invoice_pdf, name='invoice_pdf'),
]