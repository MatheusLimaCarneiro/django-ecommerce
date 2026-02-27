from rest_framework import viewsets
from .models import Category
from .serializer import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]