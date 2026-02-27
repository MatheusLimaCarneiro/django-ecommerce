from rest_framework import viewsets, mixins
from .models import CustomerProfile
from .serializer import CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated

class CustomerProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)