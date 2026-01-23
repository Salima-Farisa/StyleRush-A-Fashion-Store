from django.db import models
from django.conf import settings
from product.models import ProductVariant

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Cart ({self.user.username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def discounted_price(self):
        """Price after discount"""
        return self.variant.get_discounted_price()

    @property
    def subtotal(self):
        """Subtotal after discount"""
        return self.discounted_price * self.quantity

    @property
    def original_subtotal(self):
        """Original price subtotal (without discount)"""
        return self.variant.price * self.quantity

    @property
    def savings(self):
        """How much saved on this item"""
        return self.original_subtotal - self.subtotal

    def __str__(self):
        return f"{self.variant} x {self.quantity}"
