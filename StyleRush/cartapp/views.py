from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from product.models import ProductVariant, Category
from .models import Cart, CartItem
from django.contrib import messages

# Create your views here.
@login_required
@never_cache
def cart_view(request):
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.subtotal for item in items)
    original_total = sum(item.original_subtotal for item in items)
    total_savings = original_total - total


    return render(request, 'user/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
        "original_total": original_total,
        "savings": total_savings,
        'categories' : categories
    })

@never_cache
@login_required
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Check stock before adding
    if variant.stock <= 0:
        messages.error(request, f"Sorry, '{variant.product.name}' is out of stock.")
        return redirect('product_detail', pk=variant.product.id)

    # Check if item already exists in the cart
    item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)

    # If already in cart, increase only if stock allows
    if not created:
        if item.quantity < variant.stock:
            item.quantity += 1
            item.save()
            messages.success(request, f"'{variant.product.name}' quantity updated in cart.")
        else:
            messages.warning(request, f"Only {variant.stock} left in stock.")
    else:
        item.quantity = 1
        item.save()
        messages.success(request, f"'{variant.product.name}' added to your cart.")

    return redirect('cart')


@never_cache
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@never_cache
@login_required
def update_cart_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    variant = item.variant

    if action == 'increase':
        if item.quantity < variant.stock:
            item.quantity += 1
            item.save()
        else:
            messages.warning(request, f"Only {variant.stock} in stock for '{variant.product.name}'.")
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            messages.info(request, f"'{variant.product.name}' removed from cart.")

    return redirect('cart')
