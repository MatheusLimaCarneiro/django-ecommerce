from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'total_amount',
        'status',
        'payment_status',
        'created_at'
    ]

    search_fields = [
        'id',
        'customer__user__username',
        'customer__user__email'
    ]

    list_filter = [
        'status',
        'payment_status',
        'created_at'
    ]

    ordering = ['-created_at']

    readonly_fields = [
        'total_amount',
        'created_at',
        'updated_at'
    ]

    list_editable = [
        'status',
        'payment_status'
    ]

    list_per_page = 10