from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import ProductVariant, Discount  # import from productapp
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def discount_list(request):
    discounts = Discount.objects.select_related('variant', 'variant__product').all()
    return render(request, 'admin_app/discount_list.html', {'discounts': discounts})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_discount(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == 'POST':
        percent = request.POST.get('percent')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        active = bool(request.POST.get('active'))

        if Discount.objects.filter(variant=variant).exists():
            messages.error(request, "Discount for this variant already exists!")
            return redirect('edit_product', product_id=variant.product.id)

        Discount.objects.create(
            variant=variant,
            percent=percent,
            start_date=start,
            end_date=end or None,
            active=active
        )
        messages.success(request, "Discount added successfully!")
        return redirect('edit_product', product_id=variant.product.id)

    return render(request, 'admin_app/add_discount.html', {'variant': variant})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_discount(request, discount_id):
    discount = get_object_or_404(Discount, id=discount_id)

    # Detect if we came from discount list page
    redirect_from_list = request.GET.get("from") == "list"

    if request.method == 'POST':
        discount.percent = request.POST.get('percent')
        discount.start_date = request.POST.get('start_date')
        discount.end_date = request.POST.get('end_date') or None
        discount.active = bool(request.POST.get('active'))

        discount.save()
        messages.success(request, "Discount updated successfully!")

        if redirect_from_list:
            return redirect('discount_list')
        
        return redirect('edit_product', product_id=discount.variant.product.id)

    return render(request, 'admin_app/edit_discount.html', {'discount': discount})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_discount(request, discount_id):
    discount = get_object_or_404(Discount, id=discount_id)
    discount.delete()
    messages.success(request, "Discount deleted successfully!")
    return redirect('edit_product', product_id=discount.variant.product.id)