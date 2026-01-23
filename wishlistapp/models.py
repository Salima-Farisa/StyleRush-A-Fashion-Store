from django.db import models
from django.conf import settings
from product.models import ProductVariant  # assuming variants are added to wishlist


# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'variant')  # Prevent duplicate wishlist entries
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} → {self.variant.product.name}"
