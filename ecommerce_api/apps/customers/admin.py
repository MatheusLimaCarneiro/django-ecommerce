from django.contrib import admin
from .models import CustomerProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'email',
        'phone',
        'city',
        'state',
        'created_at'
    ]

    search_fields = [
        'user__username',
        'user__email',
        'phone',
        'city',
        'state'
    ]

    list_filter = [
        'state',
        'city',
        'created_at'
    ]

    ordering = ['-created_at']

    readonly_fields = ['created_at']

    list_per_page = 20

    # 👇 campos customizados (boa prática)
    def email(self, obj):
        return obj.user.email