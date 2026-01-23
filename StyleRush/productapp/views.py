from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Min
from product.models import Product, Brand, Category, ProductColor, ProductSize, ProductVariant  # import from productapp
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def products_page(request):
    q = request.GET.get('q')

    products = Product.objects.prefetch_related('variants').annotate(total_stock=Sum('variants__stock'),min_price=Min('variants__price'))

    if q:
        products = products.filter(name__icontains=q)

    for p in products:
        p.status = "Available" if (p.total_stock or 0) > 0 else "Out of Stock"

    return render(request, 'admin_app/products.html', {'products': products})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    colors = ProductColor.objects.all()
    sizes = ProductSize.objects.all()
    variants = product.variants.all()

    if request.method == 'POST':
        # --- Update Product Base Info ---
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category_id = request.POST.get('category')
        product.brand_id = request.POST.get('brand')
        product.featured = True if request.POST.get('featured') == 'on' else False

        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()

        # --- Update Existing Variants ---
        for variant in variants:
            price = request.POST.get(f'price_{variant.id}')
            stock = request.POST.get(f'stock_{variant.id}')
            if price is not None:
                variant.price = price
            if stock is not None:
                variant.stock = stock
            if f'image_{variant.id}' in request.FILES:
                variant.image = request.FILES[f'image_{variant.id}']
            variant.save()

        # --- Add New Variant (if provided) ---
        new_color = request.POST.get('new_color')
        new_size = request.POST.get('new_size')
        new_price = request.POST.get('new_price')
        new_stock = request.POST.get('new_stock')
        new_image = request.FILES.get('new_image')

        if new_color and new_size and new_price:
            ProductVariant.objects.create(
                product=product,
                color_id=new_color,
                size_id=new_size,
                price=new_price,
                stock=new_stock or 0,
                image=new_image
            )

        messages.success(request, 'Product and variants updated successfully!')
        return redirect('products')

    return render(request, 'admin_app/edit_product.html', {
        'product': product,
        'categories': categories,
        'brands': brands,
        'colors': colors,
        'sizes': sizes,
        'variants': variants,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('products')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        image = request.FILES.get('image')
        featured = True if request.POST.get('featured') == 'on' else False

        if not name or not category_id:
            messages.error(request, "Product name and category are required.")
            return redirect('add_product')

        # Create the product
        product = Product.objects.create(
            name=name,
            description=description,
            category_id=category_id,
            brand_id=brand_id if brand_id else None,
            featured=featured
        )

        # Optional: attach image to first variant later, or store as main image
        if image:
            # You can store it on the first color later, or extend Product model to have a main image
            pass  

        messages.success(request, f"Product '{product.name}' created successfully! Now add its variants.")
        return redirect('add_variants', product_id=product.id)

    context = {
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'admin_app/add_product.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_variants(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    colors = ProductColor.objects.all()
    sizes = ProductSize.objects.all()

    if request.method == 'POST':
        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        # Validate inputs
        if not color_id or not size_id:
            messages.error(request, "Please select both color and size.")
            return redirect('add_variants', product_id=product.id)

        # Check duplicate
        if ProductVariant.objects.filter(
            product=product, color_id=color_id, size_id=size_id
        ).exists():
            messages.warning(request, "This variant already exists!")
        else:
            ProductVariant.objects.create(
                product=product,
                color_id=color_id,
                size_id=size_id,
                price=price,
                stock=stock,
                image=image
            )
            messages.success(request, "Variant added successfully!")

        return redirect('add_variants', product_id=product.id)

    variants = ProductVariant.objects.filter(product=product)
    return render(request, 'admin_app/add_variant.html', {
        'product': product,
        'colors': colors,
        'sizes': sizes,
        'variants': variants,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_variant(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product.id
    variant.delete()
    messages.success(request, 'Variant deleted successfully!')
    return redirect('edit_product', product_id=product_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def update_variant_image(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product.id

    image = request.FILES.get("image")

    if not image:
        messages.error(request, "Please select an image.")
        return redirect('edit_product', product_id=product_id)

    variant.image = image
    variant.save()

    messages.success(request, "Variant image updated successfully!")
    return redirect('edit_product', product_id=product_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def update_variant_price(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product.id

    new_price = request.POST.get("price")
    if not new_price:
        messages.error(request, "Price cannot be empty.")
        return redirect('edit_product', product_id=product_id)

    variant.price = new_price
    variant.save()

    messages.success(request, "Price updated successfully!")
    return redirect('edit_product', product_id=product_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def update_variant_stock(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product.id

    new_stock = request.POST.get("stock")
    if new_stock is None:
        messages.error(request, "Stock cannot be empty.")
        return redirect('edit_product', product_id=product_id)

    variant.stock = new_stock
    variant.save()

    messages.success(request, "Stock updated successfully!")
    return redirect('edit_product', product_id=product_id)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def add_variant_from_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    color = request.POST.get('color')
    size = request.POST.get('size')
    price = request.POST.get('price')
    stock = request.POST.get('stock')
    image = request.FILES.get('image')

    if not color or not size or not price or not stock:
        messages.error(request, "All fields are required.")
        return redirect('edit_product', product_id=product_id)

    # Prevent duplicate
    if ProductVariant.objects.filter(product=product, color_id=color, size_id=size).exists():
        messages.warning(request, "This variant already exists.")
        return redirect('edit_product', product_id=product_id)

    ProductVariant.objects.create(
        product=product,
        color_id=color,
        size_id=size,
        price=price,
        stock=stock,
        image=image
    )

    messages.success(request, "Variant added successfully!")
    return redirect('edit_product', product_id=product_id)
