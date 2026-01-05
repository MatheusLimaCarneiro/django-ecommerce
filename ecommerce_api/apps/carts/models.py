from django.db import models
from apps.customers.models import CustomerProfile

class Cart(models.Model):
    user = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['id']

    
    def __str__(self):
        return "Cart of {}".format(self.user)