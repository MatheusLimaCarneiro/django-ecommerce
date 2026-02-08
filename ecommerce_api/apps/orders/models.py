from django.db import models
from apps.customers.models import CustomerProfile
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(
        "Total",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
        )
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING, verbose_name="status do pedido")
    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'
        REFUNDED = 'REFUNDED', 'Refunded'
    payment_status = models.CharField("Status do pagamento",max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_amount(self):
        total = self.order_items.aggregate(
            total_amount=Sum('subtotal')
        )['total_amount'] or 0
        self.total_amount = total
        self.save()

    def mark_as_paid(self):
        if self.payment_status != self.PaymentStatus.UNPAID:
            raise ValidationError("Only unpaid orders can be marked as paid.")

        self.payment_status = self.PaymentStatus.PAID
        self.status = self.Status.CONFIRMED
        self.save(update_fields=['payment_status', 'status'])
        
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f"Order {self.id} for {self.customer}"