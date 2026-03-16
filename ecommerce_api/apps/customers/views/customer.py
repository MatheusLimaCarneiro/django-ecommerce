from rest_framework import viewsets, mixins
from ..models import CustomerProfile
from ..serializers.customer import CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class CustomerProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        customer = CustomerProfile.objects.get(user=request.user)
        serializer = self.get_serializer(customer)
        return Response(serializer.data)