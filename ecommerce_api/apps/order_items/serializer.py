from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):

    unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only = True
    )

    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price', 'subtotal']