from rest_framework import viewsets, mixins
from .models import Cart
from .serializer import CartSerializer
from rest_framework.permissions import IsAuthenticated

class CartViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user__user=self.request.user)