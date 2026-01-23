from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Brand, Category, ProductColor, ProductSize  # import from productapp
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f"Category '{name}' added successfully!")
        else:
            messages.error(request, "Category name cannot be empty.")
    return redirect('categories')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    name = request.POST.get("name")
    image = request.FILES.get("image")

    if name:
        category.name = name
    if image:
        category.image = image

    category.save()
    messages.success(request, "Category updated successfully!")
    return redirect('categories')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")

    return redirect('categories')
    

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_brand(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            Brand.objects.create(name=name)
            messages.success(request, f"Brand '{name}' added successfully!")
    return redirect('brands')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)

    name = request.POST.get("name")
    logo = request.FILES.get("logo")
    website = request.POST.get("website")

    if name:
        brand.name = name

    if logo:
        brand.logo = logo

    if website:
        brand.website = website

    brand.save()
    messages.success(request, "Brand updated successfully!")
    return redirect('brands')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brand.delete()
    messages.success(request, "Brand deleted successfully!")

    return redirect('brands')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_color(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ProductColor.objects.create(name=name)
            messages.success(request, f"Color '{name}' added successfully!")
    return redirect('colors')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def edit_color(request, color_id):
    color = get_object_or_404(ProductColor, id=color_id)

    name = request.POST.get("name")
    image = request.FILES.get("image")
    code = request.POST.get("code")

    if name:
        color.name = name

    if image:
        color.main_image = image

    if code:
        color.color_code = code

    color.save()
    messages.success(request, "Color updated successfully!")
    return redirect('colors')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_color(request, color_id):
    color = get_object_or_404(ProductColor, id=color_id)
    color.delete()
    messages.success(request, "Color deleted successfully!")

    return redirect('colors')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_size(request):
    if request.method == 'POST':
        size = request.POST.get('size')
        if size:
            ProductSize.objects.create(size=size)
            messages.success(request, f"Size '{size}' added successfully!")
    return redirect('size')

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def edit_size(request, size_id):
    size = get_object_or_404(ProductSize, id=size_id)

    name = request.POST.get("size")

    if name:
        size.size = name

    size.save()
    messages.success(request, "Size updated successfully!")
    return redirect('size')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_size(request, size_id):
    size = get_object_or_404(ProductSize, id=size_id)
    size.delete()
    messages.success(request, "Size deleted successfully!")

    return redirect('size')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories = Category.objects.all()
    q = request.GET.get('q')
    if q:
        categories = categories.filter(name__icontains=q)
    return render(request, 'admin_app/categories.html', {'categories': categories})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def brands(request):
    brands = Brand.objects.all()
    q = request.GET.get('q')
    if q:
        brands = brands.filter(name__icontains=q)
    return render(request, 'admin_app/brands.html', {'brands': brands})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def colors(request):
    colors = ProductColor.objects.all()
    return render(request, 'admin_app/colors.html' , {'colors': colors})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def sizes(request):
    sizes = ProductSize.objects.all()
    return render(request, 'admin_app/size.html' , {'sizes': sizes})