from rest_framework import viewsets, mixins
from .models import Cart
from .serializer import CartSerializer
from apps.orders.models import Order
from apps.order_items.models import OrderItem
from apps.orders.serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from .exceptions import EmptyCartException, InsufficientStockException

class CartViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer= self.request.user.customerprofile)

    # Override list to return the current user's cart or create one if it doesn't exist instead of a list of carts.
    # This is because each user should only have one cart, so listing all carts doesn't make sense in this context.
    def list(self, request, *args, **kwargs):
        customer = request.user.customerprofile

        cart, _ = Cart.objects.get_or_create(customer=customer)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def checkout(self, request, pk=None):
        """
        Converts a Cart into an Order.

        Creates an Order for the cart's customer and converts each CartItem
        into an OrderItem using the price stored at the time the item was
        added to the cart. After the order is created, the cart is cleared.
        """
        cart = self.get_object()

        # Prevent checkout if the cart is empty
        if not cart.items.exists():
            raise EmptyCartException()
        
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                raise InsufficientStockException(
                    detail=f"Not enough stock for product '{item.product.name}'"  
                )

        with transaction.atomic():
            order = Order.objects.create(customer=cart.customer)
            
            for item in cart.items.all():
                order_item = OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
                # Use the price stored when the item was added to the cart
                # to avoid inconsistencies if the product price changes later.
                order_item.calculate_prices(item.price_at_time)
                order_item.save()

            order.update_total_amount()

            # Clear the cart after successful checkout
            cart.items.all().delete()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )