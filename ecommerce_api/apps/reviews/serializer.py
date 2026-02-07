from rest_framework import serializers
from .models import Review
from apps.order_items.models import OrderItem

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'rating', 'comment', 'created_at']
        read_only_fields = ['product', 'customer', 'created_at']

    def validate(self, data):
        product = self.context.get('product')
        
        if not product:
            raise serializers.ValidationError(
                {"Product data is required to validate the review."}
            )
        
        customer  = self.context.get('customer')
        
        if not customer:
            raise serializers.ValidationError(
                {"Customer data is required to validate the review."}
            )
        
        rating = data.get('rating')

        if rating is None or not 1 <= rating <= 5:
            raise serializers.ValidationError(
                {"Rating must be between 1 and 5."}
            )

        purchased = OrderItem.objects.filter(
            order__customer=customer,
            order__payment_status = 'PAID',
            product=product
        )

        if not purchased.exists():
            raise serializers.ValidationError(
                {"Customer must have purchased the product to leave a review."}
            )

        if Review.objects.filter(product=product, customer=customer).exists():
            raise serializers.ValidationError(
                {"A review by this customer for this product already exists."}
            )

        return data

    def create(self, validated_data):
        product = self.context.get('product')
        customer = self.context.get('customer')

        review = Review.objects.create(
            product=product,
            customer=customer,
            rating=validated_data['rating'],
            comment=validated_data.get('comment', ''),
        )
        return review