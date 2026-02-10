from rest_framework import viewsets, mixins
from .models import OrderItem
from .serializer import OrderItemSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class OrderItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return OrderItem.objects.none()

        return OrderItem.objects.filter(
            order__customer__user=self.request.user
        )