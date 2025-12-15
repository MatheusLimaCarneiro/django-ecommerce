from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("The price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("The inventory cannot be negative.")
        return value

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'stock', 'is_active', 'created_at', 'updated_at']