from django.db import models
from django.core.validators import MinValueValidator
from apps.carts.models import Cart
from apps.products.models import Product

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name= 'items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(
        "Quantidade",
        validators=[MinValueValidator(1)]
    )
    price_at_time = models.DecimalField(
        "Preço no momento",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Items do Carrinho"
        ordering = ['id']
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} X {self.product}"