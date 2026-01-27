from django.db import models
from apps.orders.models import Order
from apps.products.models import Product
from django.core.validators import MinValueValidator

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(
        "Quantidade",
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        "Preço no unitario",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        "Subtotal",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_product_per_order'
            )
        ]

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"