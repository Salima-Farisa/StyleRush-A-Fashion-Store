from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from orderapp.models import Order
from decimal import Decimal
from django.contrib import messages
from django.utils import timezone
from product.models import Category
from django.views.decorators.cache import never_cache
from walletapp.models import Wallet
from invoice.models import Invoice

# Create your views here.

@login_required
@never_cache
def order_success(request, order_id):
    categories = Category.objects.all()

    order = get_object_or_404(Order, id=order_id, user=request.user)
    shipping_charge = Decimal('12.00')  # 👈 convert to Decimal
    total_with_shipping = order.total + shipping_charge

    context = {
        'order': order,
        'order_date': order.created_at.strftime("%d-%m-%y"),
        'shipping_charge': shipping_charge,
        'total_with_shipping': total_with_shipping,
        'categories': categories
    }
    return render(request, 'user/order_success.html', context)


@login_required
@never_cache
def order_page(request):
    categories = Category.objects.all()

    orders = (
        Order.objects
        .filter(user=request.user)
        .select_related('address')
        .prefetch_related('items__variant__product')
        .order_by('-created_at')
    )
    return render(request, 'user/orders.html', {'orders': orders, 'categories': categories})

@login_required
@never_cache
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prevent re-cancellation
    if order.payment_status == 'Cancelled':
        messages.info(request, 'This order is already cancelled.')
        return redirect('order_list')

    # Allow cancellation only if Pending or Paid
    if order.payment_status in ['Pending', 'Paid', 'Processing']:

        # ✅ CREDIT WALLET (only if paid online or wallet)
        if order.payment_status == 'Paid'and order.payment_mode in ['UPI', 'wallet']:
            wallet, _ = Wallet.objects.get_or_create(user=request.user)
            wallet.balance += order.total
            wallet.save()

            messages.success(request, f'₹{order.total} has been refunded to your wallet.')
        
        order.payment_status = 'Cancelled'
        # Optional: track when it was cancelled
        if hasattr(order, 'cancelled_at'):
            order.cancelled_at = timezone.now()
        order.save()
        messages.success(request, '✅ Your order has been cancelled successfully.')
    else:
        messages.warning(
            request,
            f'🚫 Cannot cancel an order that is already {order.payment_status.lower()}.'
        )

    return redirect('order_list')

@login_required
@never_cache
def track_order(request, order_id):
    """Display order tracking page with timeline"""

    categories = Category.objects.all()
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Example tracking flow
    tracking_steps = [
        {'name': 'Order Placed', 'status': order.created_at, 'done': True},
        {'name': 'Confirmed', 'status': order.confirmed_at if hasattr(order, 'confirmed_at') else None, 'done': order.payment_status in ['Confirmed', 'Shipped', 'Delivered']},
        {'name': 'Shipped', 'status': order.shipped_at if hasattr(order, 'shipped_at') else None, 'done': order.payment_status in ['Shipped', 'Delivered']},
        {'name': 'Delivered', 'status': order.delivered_at if hasattr(order, 'delivered_at') else None, 'done': order.payment_status == 'Delivered'},
    ]

    context = {
        'order': order,
        'tracking_steps': tracking_steps,
        'categories': categories
    }
    return render(request, 'user/track_order.html', context)


@login_required
@never_cache
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related('address'), id=order_id, user=request.user)

    # 🔥 ALWAYS create/get invoice
    invoice, created = Invoice.objects.get_or_create(
        order=order,
        defaults={
            "invoice_number": f"INV-{order.id}",
            "customer_name": f"{order.address.first_name} {order.address.last_name}",
            "customer_email": request.user.email,
            "billing_address": str(order.address),
            "total_amount": order.total,
        }
    )

    categories = Category.objects.all()

    return render(
        request,
        "user/order_detail.html",
        {
            "order": order,
            "invoice": invoice,
            "categories": categories,
        }
    )
