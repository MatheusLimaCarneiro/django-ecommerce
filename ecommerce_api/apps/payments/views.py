from .models import Payment
from .serializer import PaymentSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Payment.objects.none()

        return Payment.objects.filter(order__customer__user = user)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        payment = self.get_object()
        
        try:
            payment.confirm_payment()
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=400
            )
        
        return Response(
            {"detail": "Payment confirmed successfully."},
            status=200
        )