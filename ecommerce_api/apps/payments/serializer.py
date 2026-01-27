from rest_framework import serializers
from .models import Payment
from django.utils import timezone

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'amount', 'status', 'paid_at', 'created_at']
        read_only_fields = ['amount','status', 'paid_at', 'created_at']

    def validate(self, data):
        order = self.context.get('order')

        if not order:
            raise serializers.ValidationError(
                {"Order data is required to validate the payment."}
            )
        
        if hasattr(order, 'payment'):
            raise serializers.ValidationError(
                {"Payment already exists for this order."}
            )

        method = data.get('method')

        if order.total_amount == 0 and method in [Payment.Method.CREDIT_CARD, Payment.Method.PAYPAL]:
            raise serializers.ValidationError(
                {"This payment method cannot be used for zero amount orders."}
            )

        return data

    def create(self, validated_data):
        order = self.context.get('order')
        
        if not order:
            raise serializers.ValidationError(
                {"Order data is required to create a payment."}
            )

        amount = order.total_amount
        status = Payment.Status.PENDING
        paid_at = None

        if amount == 0:
            status = Payment.Status.PAID
            paid_at = timezone.now()

        payment = Payment.objects.create(
            order=order,
            method=validated_data['method'],
            amount=amount,
            status=status,
            paid_at = paid_at
        )
        return payment