from rest_framework import viewsets
from .models import Cart
from .serializer import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ["get", "post", "delete"]