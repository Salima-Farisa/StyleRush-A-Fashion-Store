from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Brand, Category, Product, Subscriber, ProductVariant
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from adminapp.models import Customer
from wishlistapp.models import Wishlist
from django.db.models import Min
from walletapp.models import Wallet

@never_cache
def home(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True).select_related('category', 'brand')[:6]

    context = {
        'brands': brands,
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'user/home.html', context)


def products_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(brand=brand)

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list("variant", flat=True)

    context = {
        'brand': brand,
        'brands' : brands,
        'categories': categories,
        'products': products,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'user/products.html', context)

def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Combine message with user info
        full_message = f"Message from {name} <{email}>:\n\n{message}"

        # (Optional) Send to your admin email
        send_mail(
            subject or "Website Contact Form",
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )

        messages.success(request, "Thank you! Your message has been sent successfully.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    customer = getattr(user, 'profile', None)

    if not customer:
        customer = Customer.objects.create(user=user)

    # ✅ Get wallet (create if not exists)
    wallet, _ = Wallet.objects.get_or_create(user=user)

    context = {
        'user': user,
        'customer': customer,
        'wallet': wallet,   # 👈 pass wallet
    }
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    customer = getattr(user, 'profile', None)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if customer:
            customer.phone = request.POST.get('phone')
            customer.address = request.POST.get('address')
            customer.country = request.POST.get('country')

            if 'profile_image' in request.FILES:
                customer.profile_image = request.FILES['profile_image']

            customer.save()

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'user': user,
        'customer': customer,
    }
    return render(request, 'user/edit_profile.html', context)


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You're already subscribed!")
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, "Thank you for subscribing!")
        return redirect('home')


def about(request):
    categories = Category.objects.all()
    return render(request, 'user/about.html', {'categories': categories})




def product_list(request, category_id=None):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    category = None

    products = Product.objects.all().select_related('category', 'brand').prefetch_related('variants__discount')

    # Filter by category
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    # Search
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)

    # Annotate for sorting
    products = products.annotate(min_price=Min('variants__price'))

    # Sorting
    sort_option = request.GET.get('sort', 'default')
    if sort_option == 'Price: Low to High':
        products = products.order_by('min_price')
    elif sort_option == 'Price: High to Low':
        products = products.order_by('-min_price')
    elif sort_option == 'Newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('id')

    # Pagination
    show_option = request.GET.get('show', '16')
    if show_option == 'All':
        paginator = Paginator(products, products.count() or 1)
    else:
        paginator = Paginator(products, int(show_option))

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Wishlist
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('variant', flat=True)

    return render(request, 'user/products.html', {
        'brands': brands,
        'categories': categories,
        'category': category,
        'products': page_obj,
        'sort_option': sort_option,
        'show_option': show_option,
        'wishlist_items': wishlist_items,
    })


def product_detail(request, pk):
    categories = Category.objects.all()
    product = get_object_or_404(
        Product.objects.prefetch_related("variants__discount"), pk=pk
    )

    variants = product.variants.select_related("color", "size").order_by("id")
    
    # Default variant
    first_variant = variants[0]
    selected_color = first_variant.color.id
    selected_size = first_variant.size.id

    # Selected variant
    selected_variant_id = request.GET.get("variant")
    if selected_variant_id:
        try:
            first_variant = variants.get(id=selected_variant_id)
            selected_color = first_variant.color.id
            selected_size = first_variant.size.id
        except ProductVariant.DoesNotExist:
            pass
        
    # ✅ UNIQUE sizes and colors (CRITICAL)
    unique_sizes = variants.values("size__id", "size__size").distinct()
    unique_colors = variants.values(
        "color__id", "color__color_code", "color__name"
    ).distinct()

    # AVAILABLE sizes for selected color
    sizes_for_selected_color = list(
        variants.filter(color_id=selected_color).values_list("size_id", flat=True)
    )

    # AVAILABLE colors for selected size
    colors_for_selected_size = list(
        variants.filter(size_id=selected_size).values_list("color_id", flat=True)
    )

    related_products = (
        Product.objects.filter(category=product.category)
        .exclude(id=product.id)
        .prefetch_related("variants__discount")
    )[:4]

    for rp in related_products:
        rp.first_variant = rp.variants.first()

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(
            user=request.user
        ).values_list("variant", flat=True)

    return render(
        request,
        "user/product_detail.html",
        {
            "product": product,
            "variants": variants,
            "first_variant": first_variant,
            "selected_color": selected_color,
            "selected_size": selected_size,
            "unique_sizes": unique_sizes,          # ✅ REQUIRED
            "unique_colors": unique_colors,        # ✅ REQUIRED
            "sizes_for_selected_color": sizes_for_selected_color,
            "colors_for_selected_size": colors_for_selected_size,
            "related_products": related_products,
            "wishlist_items": wishlist_items,
            "categories": categories,
        },
    )


def custom_404(request, exception):
    return render(request, 'user/404.html')