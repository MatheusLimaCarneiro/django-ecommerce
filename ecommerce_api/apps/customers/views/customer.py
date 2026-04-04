from rest_framework import viewsets
from ..models import CustomerProfile
from ..serializers.customer import CustomerProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class CustomerProfileViewSet(viewsets.GenericViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomerProfile, user=self.request.user)

    @action(detail=False, methods=["GET", "PATCH"])
    def me(self, request):
        customer = self.get_object()
        
        if request.method == "GET":
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        
        elif request.method == "PATCH":
            serializer = self.get_serializer(customer, data=request.data, partial=True)
            
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status= status.HTTP_200_OK)