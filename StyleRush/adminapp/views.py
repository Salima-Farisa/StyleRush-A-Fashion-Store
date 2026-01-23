from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Customer
from orderapp.models import Order
from django.db.models import Sum, Min
from django.contrib import messages
from product.models import Product  # import from productapp
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from walletapp.models import Wallet

# Create your views here.
@never_cache
def login_admin(request):
    # If already logged in and is superuser, go directly to dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Access denied! Only admins can log in here.")
                return redirect('admin_login')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login_admin')

    return render(request, 'admin_app/login.html')

def admin_logout(request):
    logout(request)
    return redirect('login_admin')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    total_orders = Order.objects.count()
    total_sales = sum(
        (item.variant.get_discounted_price() * item.quantity)
        for order in Order.objects.prefetch_related('items__variant__discount')
        for item in order.items.all()
        if item.variant is not None
    )

    total_customers = Customer.objects.count()
    top_products = (
        Product.objects.annotate(
            total_stock=Sum('variants__stock'),
            min_price=Min('variants__price')
        )
        .order_by('-total_stock')[:5]
    )

    recent_orders = (
        Order.objects
        .select_related('user', 'address')
        .prefetch_related('items__variant__product')
        .order_by('-id')[:5]
    )

    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_customers': total_customers,
        'top_products': top_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_app/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def profile_view(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'admin_app/profile.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_profile(request):
    user = request.user
    customer = getattr(user, 'profile', None)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')


        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('admin_profile')

    context = {
        'user': user,
        'customer': customer,
    }
    return render(request, 'admin_app/edit_profile.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def orders_page(request):
    orders = (
        Order.objects
        .select_related('user', 'address')
        .prefetch_related('items__variant__product')
        .order_by('-id')
    )

    return render(request, 'admin_app/orders.html', {'orders': orders})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def update_order_status(request, order_id):
    """
    Admin view: Update order status (Pending → Shipped → Delivered, etc.)
    Prevent updates if order is Cancelled or Delivered.
    """
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    valid_statuses = ['Pending', 'Paid', 'Shipped', 'Delivered', 'Cancelled']

    # Restrict updates if order already Cancelled or Delivered
    if order.payment_status in ['Cancelled', 'Delivered']:
        messages.warning(
            request, f"Order #{order.id} cannot be updated because it is already {order.payment_status.lower()}."
        )
        return redirect('orders')

    if new_status in valid_statuses:
        order.payment_status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {new_status}.")
    else:
        messages.error(request, "Invalid order status selected.")

    return redirect('orders')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def customers(request):
    customers = Customer.objects.select_related('user').all()
    return render(request, 'admin_app/customers.html', {'customers': customers})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    wallet, _ = Wallet.objects.get_or_create(user=customer.user)

    return render(request, 'admin_app/customer_detail.html', {
        'customer': customer,
        'wallet': wallet
    })
