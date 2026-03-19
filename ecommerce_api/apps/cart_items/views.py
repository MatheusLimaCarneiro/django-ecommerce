from rest_framework import viewsets
from .models import CartItem
from apps.carts.models import Cart
from .serializer import CartItemSerializer
from rest_framework.permissions import IsAuthenticated

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)

    # Override create to associate the new CartItem with the current user's cart.
    # This ensures that when a user adds an item to their cart, it is automatically linked to their cart without needing to specify the cart in the request data.
    def perform_create(self, serializer):
        customer = self.request.user.profile

        cart, _ = Cart.objects.get_or_create(customer=customer)

        serializer.save(cart=cart)