from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import ProductVariant, Category
from .models import Wishlist
from django.views.decorators.cache import never_cache

# Create your views here.
@login_required
@never_cache
def wishlist_page(request):
    """
    Show all wishlist items for the logged-in user.
    """
    categories = Category.objects.all()
    wishlist_items = (
        Wishlist.objects
        .filter(user=request.user)
        .select_related('variant__product')
        .order_by('-added_at')
    )
    return render(request, 'user/wishlist.html', {'wishlist_items': wishlist_items, 'categories': categories})


@login_required
@never_cache
def add_to_wishlist(request, variant_id):
    """
    Add a product variant to wishlist.
    """
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if Wishlist.objects.filter(user=request.user, variant=variant).exists():
        messages.info(request, "This item is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, variant=variant)
        messages.success(request, "Added to your wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'wishlist_page'))


@login_required
@never_cache
def remove_from_wishlist(request, variant_id):
    item = get_object_or_404(Wishlist, variant_id=variant_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from your wishlist.")
    
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_page'))
