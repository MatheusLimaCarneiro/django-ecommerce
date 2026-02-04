from .models import Review
from .serializer import ReviewSerializer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product__is_active=True)