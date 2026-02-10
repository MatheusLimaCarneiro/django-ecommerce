from rest_framework import viewsets, mixins
from .models import Order
from .serializer import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from apps.payments.serializer import PaymentSerializer
from apps.order_items.serializer import OrderItemSerializer

class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["payments", "item"]:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    @action(detail=True, methods=["POST"])
    def payments(self, request, pk=None):
        order = self.get_object()

        serializer = PaymentSerializer(
            data=request.data,
            context={"order": order}
        )
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["POST"], url_path='items')
    def item(self, request, pk=None):
        order = self.get_object()

        if order.customer.user != request.user:
            return Response(
                {"detail": "You do not have permission to add items to this order."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status != Order.Status.PENDING:
            return Response(
                {"detail": "Cannot add items to an order that is not pending."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.payment_status == Order.PaymentStatus.PAID:
            return Response(
                {"detail": "Cannot add items to an order that has been paid."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OrderItemSerializer(data = request.data, context={"order": order})
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()

        return Response(
            OrderItemSerializer(order_item).data,
            status=status.HTTP_201_CREATED
        )