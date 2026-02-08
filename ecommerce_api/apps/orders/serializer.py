from rest_framework import serializers
from .models import Order
from apps.customers.models import CustomerProfile

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'payment_status', 'total_amount', 'created_at', 'updated_at']
        read_only_fields = [ 'status','payment_status', 'total_amount', 'customer']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user or user.is_anonymous:
            raise serializers.ValidationError(
                {"user": "Authentication required to create an order."}
            )

        try:
            customer_profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            raise serializers.ValidationError(
                {"customer": "Customer profile not found for this user."}
            )

        order = Order.objects.create(
            customer=customer_profile,
        )

        return order