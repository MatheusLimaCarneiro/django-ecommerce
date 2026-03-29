from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['price_at_time']
    fields = ['product', 'quantity', 'price_at_time']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'updated_at']
    
    search_fields = [
        'customer__user__username',
        'customer__user__email'
    ]

    ordering = ['-updated_at']

    readonly_fields = ['created_at', 'updated_at']

    inlines = [CartItemInline]

    list_select_related = ['customer', 'customer__user']

    list_per_page = 20


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'price_at_time']

    search_fields = [
        'product__name',
        'cart__customer__user__username'
    ]

    list_filter = [
        'product',
        'cart__customer'
    ]

    readonly_fields = ['price_at_time']

    list_select_related = ['cart', 'product']

    ordering = ['-id']

    list_per_page = 20