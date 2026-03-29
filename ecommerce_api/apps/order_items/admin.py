from django.contrib import admin
from .models import OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    def order_info(self, obj):
        return f"#{obj.order.id} - {obj.order.customer.user.username}"

    order_info.short_description = "Order"
    
    list_display = [
        'id',
        'order_info',
        'product',
        'quantity',
        'unit_price',
        'subtotal'
    ]

    search_fields = [
        'order__id',
        'product__name'
    ]

    list_filter = [
        'order__status',
        'order__payment_status',
        'product'
    ]

    ordering = ['-id']

    readonly_fields = [
        'subtotal',
        'unit_price'
    ]

    list_per_page = 10