from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Address
from cartapp.models import CartItem
from django.contrib import messages
from orderapp.models import Order  
from decimal import Decimal
from product.models import Category
from walletapp.models import Wallet
from django.db import transaction

# Create your views here.
@never_cache
@login_required
def select_address(request):
    addresses = Address.objects.filter(user=request.user)
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total = sum(item.subtotal for item in cart_items)
    categories = Category.objects.all()

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        if selected_address_id:
            request.session['selected_address'] = selected_address_id
            return redirect('billing_page')

    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'total': total,
        'categories' : categories
    }
    return render(request, 'user/checkout_select_address.html', context)

@never_cache
@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            street_address=request.POST.get('street_address'),
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            country=request.POST.get('country'),
            is_default=bool(request.POST.get('is_default')),
        )
        return redirect('checkout')  # Redirect back to the same page
    
@never_cache
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('checkout')

@transaction.atomic
@never_cache
@login_required
def billing_page(request):
    categories = Category.objects.all()
    # Get selected address from session (from checkout/select_address step)
    address_id = request.session.get('selected_address')
    if not address_id:
        messages.warning(request, "Please select a shipping address first.")
        return redirect('checkout')  # redirect back to address selection

    address = get_object_or_404(Address, id=address_id, user=request.user)

    # Fetch user's cart items
    cart_items = CartItem.objects.filter(cart__user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate total price
    total = sum(Decimal(item.subtotal) for item in cart_items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id')
        upi_app = request.POST.get('upi_app')

        # 🔹 WALLET PAYMENT
        if payment_method == "WALLET":
            wallet, _ = Wallet.objects.get_or_create(user=request.user)

            if wallet.balance < total:
                messages.error(request, "Insufficient wallet balance.")
                return redirect('billing_page')

            # ✅ DEBIT WALLET
            wallet.balance -= total
            wallet.save()

            payment_status = "Paid"

        elif payment_method == "UPI":
            payment_status = "Paid"
        else:
            payment_status = "Pending"

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total=total,
            payment_mode=payment_method,
            payment_status=payment_status,
            upi_id=upi_id if payment_method == 'UPI' else None,
            upi_app=upi_app if payment_method == 'UPI' else None,
        )

        # Optionally add the ordered items
        for item in cart_items:
                variant=item.variant

                if variant.stock < item.quantity:
                    messages.error(request, f"Not enough stock for {variant.product.name}")
                    return redirect('cart')

                 # ✅ REDUCE STOCK    
                variant.stock -=item.quantity
                variant.save()

                # ✅ CREATE ORDER ITEM
                order.items.create(
                    variant=variant,
                    quantity=item.quantity,
                    price=variant.price,
                )  

        # Clear cart after placing order
        cart_items.delete()

        # Success message & redirect
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success', order_id=order.id)

    context = {
        'address': address,
        'cart_items': cart_items,
        'total': total,
        'categories' : categories
    }
    return render(request, 'user/checkout_billing.html', context)