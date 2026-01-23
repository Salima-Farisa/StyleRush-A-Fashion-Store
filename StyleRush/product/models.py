from django.db import models
from django.utils import timezone


# Create your models here.
# Brand

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# Category

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

# Product (Base item)

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/main/', blank=True, null=True)

    def __str__(self):
        return self.name


# ProductColor (Each color option for a product)

class ProductColor(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, help_text="HEX code like #ff0000", blank=True, null=True)
    main_image = models.ImageField(upload_to='products/colors/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


# ProductSize(Each size per color)

class ProductSize(models.Model):
    size=models.CharField(max_length=5)

    def __str__(self):
        return self.size

# ProductVariant ( Product with stock & price)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/variants/', blank=True, null=True)

    class Meta:
        unique_together = ('product','color', 'size')  # Prevent duplicate combinations

    def get_discounted_price(self):
        if hasattr(self, 'discount') and self.discount.is_active():
            discount_value = (self.price * self.discount.percent) / 100
            return round(self.price - discount_value, 2)
        return self.price

    def has_active_discount(self):
        """Check if this variant currently has an active discount."""
        return hasattr(self, 'discount') and self.discount.is_active()

    def __str__(self):
        return f"{self.product.name} - {self.color.name} / {self.size}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Discount(models.Model):
    variant = models.OneToOneField('ProductVariant',on_delete=models.CASCADE,related_name='discount')
    percent = models.DecimalField(max_digits=5, decimal_places=2,)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def is_active(self):
        """Check if discount is active and within date range."""
        now = timezone.now()
        return self.active and self.start_date <= now and (self.end_date is None or now <= self.end_date)

    def __str__(self):
        return f"{self.variant.product.name} ({self.percent}% off)"

    