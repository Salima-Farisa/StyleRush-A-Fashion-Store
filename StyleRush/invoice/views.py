from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.template.loader import render_to_string 
from weasyprint import HTML 
from .models import Invoice
from django.shortcuts import get_object_or_404 

# Create your views here.
@login_required
def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        order__user=request.user
    )

    items = invoice.order.items.all()

    html_string = render_to_string(
        "user/invoice_pdf.html",
        {
            "invoice": invoice,
            "order": invoice.order,
            "items": items,
        }
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    )

    HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/")
    ).write_pdf(response)

    return response
