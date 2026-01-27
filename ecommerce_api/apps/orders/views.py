from rest_framework import viewsets, mixins
from .models import Order
from .serializer import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.payments.serializer import PaymentSerializer

class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == "payments":
            return [IsAuthenticated()]
        return []

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