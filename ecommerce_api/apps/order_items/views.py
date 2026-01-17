from rest_framework import viewsets, mixins
from .models import OrderItem
from .serializer import OrderItemSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class OrderItemViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]