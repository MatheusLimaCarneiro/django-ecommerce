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
        fields = ['id', 'order', 'product', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price', 'subtotal']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if not product.is_active:
            raise serializers.ValidationError("Product is inactive.")

        if product.stock <= 0:
            raise serializers.ValidationError("Product is out of stock.")

        if quantity > product.stock:
            raise serializers.ValidationError("Insufficient stock.")

        return data

    def create(self, validated_data):
       product = validated_data['product']
       quantity = validated_data['quantity']
       
       validated_data['unit_price'] = product.price
       validated_data['subtotal'] = product.price * quantity
       
       return super().create(validated_data)