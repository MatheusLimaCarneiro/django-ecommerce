from .models import Payment
from .serializer import PaymentSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

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
        
        if payment.status != 'PENDING':
            return Response({'detail': 'Payment already confirmed or failed.'}, status=400)
        
        payment.status = 'PAID'
        payment.paid_at = timezone.now()
        payment.save()

        return Response({'detail': 'Payment confirmed successfully.'})