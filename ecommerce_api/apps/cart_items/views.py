from rest_framework import viewsets
from .models import CartItem
from .serializer import CartItemSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer