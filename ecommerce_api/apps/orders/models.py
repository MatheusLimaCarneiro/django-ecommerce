from django.db import models
from apps.customers.models import CustomerProfile
from django.core.validators import MinValueValidator
from django.db.models import Sum

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(
        "Total",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
        )
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING', verbose_name="status do pedido")
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('REFUNDED', 'Refunded'),
    ]
    payment_status = models.CharField("Status do pagamento",max_length=50, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_amount(self):
        total = self.order_items.aggregate(
            total_amount=Sum('subtotal')
        )['total_amount'] or 0
        self.total_amount = total
        self.save()
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f"Order {self.id} for {self.customer}"