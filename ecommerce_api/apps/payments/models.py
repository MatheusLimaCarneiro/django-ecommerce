from django.db import models
from apps.orders.models import Order
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    class Method(models.TextChoices):
            CREDIT_CARD = 'CREDIT_CARD', _('Credit Card')
            PAYPAL = 'PAYPAL', _('PayPal')
            PIX = 'PIX', _('Pix')
    class Status(models.TextChoices):
            PENDING = 'PENDING', _('Pending')
            PAID = 'PAID', _('Paid')
            FAILED = 'FAILED', _('Failed')
            REFUNDED = 'REFUNDED', _('Refunded')
    method = models.CharField(_("Payment Method"), max_length=50, choices=Method.choices)
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
        )
    status = models.CharField(_("Payment Status"), max_length=50, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.amount == 0 and self.method in [self.Method.CREDIT_CARD, self.Method.PAYPAL]:
            raise ValidationError({
                'method': "This payment method cannot be used for zero amount orders."
            })

    def __str__(self):
        return f"Payment #{self.id} | Order #{self.order_id} | {self.method} | {self.status}"