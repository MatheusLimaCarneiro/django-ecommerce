from rest_framework import viewsets
from .models import CustomerProfile
from .serializer import CustomerProfileSerializer

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer