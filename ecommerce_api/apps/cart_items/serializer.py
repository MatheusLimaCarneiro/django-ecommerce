from rest_framework import serializers
from .models import CartItem
from apps.products.models import Product

class CartItemSerializer(serializers.ModelSerializer):

    price_at_time = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only = True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'price_at_time']
        validators = [] 

    def validate(self, data):
        product = data.get("product") or getattr(self.instance, "product", None)
        quantity = data.get("quantity") or getattr(self.instance, "quantity", None)

        if not product:
            return data

        if isinstance(product, int):
            product = Product.objects.get(pk=product)

        if not product.is_active:
            raise serializers.ValidationError(
                "Product is inactive."
            )
        
        if product.stock <= 0:
            raise serializers.ValidationError(
                "Product is out of stock."
            )
        
        if quantity and quantity > product.stock:
            raise serializers.ValidationError("Requested quantity exceeds available stock.")

        return data

    def create(self, validated_data):
        cart = validated_data["cart"]
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        existing = CartItem.objects.filter(cart=cart, product=product).first()

        if existing:
            total = existing.quantity + quantity

            if total > product.stock:
                raise serializers.ValidationError(
                    "Requested quantity exceeds available stock."
                )
            existing.quantity = total
            existing.save()
            return existing

        validated_data["price_at_time"] = product.price
        
        cart_item = CartItem.objects.create(**validated_data)
        return cart_item