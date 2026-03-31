from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price',
        'stock',
        'is_active',
        'category',
        'created_at'
    ]

    search_fields = ['name']
    
    list_filter = [
        'category',
        'is_active'
    ]
    
    ordering = ['-stock']

    list_editable = [
        'price',
        'stock',
        'is_active']
    
    list_per_page = 10

    readonly_fields = ['created_at']