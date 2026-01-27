from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'order_items'

router = routers.DefaultRouter()
router.register('', views.OrderItemViewSet, basename='orderitem')
urlpatterns = [
    path('', include(router.urls)),
]