from django.urls import path, include
from rest_framework import routers
from . import views 

app_name = 'products'

router = routers.DefaultRouter()
router.register('', views.ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]