from rest_framework import viewsets
from .models import Product
from .serializer import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.customers.models import CustomerProfile
from apps.reviews.serializer import ReviewSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == "reviews":
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=True, methods=["POST"])
    def reviews(self, request, pk=None):
        product = self.get_object()

        try:
            customer = request.user.profile
        except CustomerProfile.DoesNotExist:
            return Response(
                {"detail": "Customer profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReviewSerializer(
            data=request.data,
            context={"request": request, "product": product, "customer": customer}
        )

        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )