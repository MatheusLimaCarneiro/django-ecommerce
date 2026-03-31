from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'customer',
        'rating',
        'created_at'
    ]

    search_fields = [
        'product__name',
        'customer__user__username',
        'customer__user__email'
    ]

    list_filter = [
        'rating',
        'product',
        'created_at'
    ]

    ordering = ['-created_at']

    readonly_fields = ['created_at']

    list_select_related = ['product', 'customer', 'customer__user']

    list_per_page = 20