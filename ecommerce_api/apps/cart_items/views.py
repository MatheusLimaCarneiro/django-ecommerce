from rest_framework import viewsets
from .models import CartItem
from .serializer import CartItemSerializer
from rest_framework.permissions import IsAuthenticated

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user__user=self.request.user)