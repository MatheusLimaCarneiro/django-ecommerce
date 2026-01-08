from django.urls import path, include
from rest_framework import routers
from . import views 

app_name = 'cart_items'

router = routers.DefaultRouter()
router.register('', views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]