from django.db import models
from apps.products.models import Product
from apps.customers.models import CustomerProfile
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        _("Rating"),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_("Rating must be between 1 and 5")
    )
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'customer'],
                name='unique_review_per_product_customer'
            )
        ]

    def __str__(self):
        return f"Review #{self.id} | Product #{self.product} | Customer #{self.customer} | Rating: {self.rating}"