from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def order_info(self, obj):
        return f"#{obj.order.id} - {obj.order.customer.user.username}"

    order_info.short_description = "Order"
    list_display = [
        'id',
        'order_info',
        'method',
        'amount',
        'status',
        'paid_at',
        'created_at'
    ]

    list_filter = ['method', 'status', 'created_at']

    search_fields = ['id', 'order__id']

    ordering = ['-created_at']

    list_editable = ['status']

    readonly_fields = ['created_at', 'paid_at']

    list_per_page = 10