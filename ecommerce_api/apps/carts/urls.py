from django.urls import path, include
from rest_framework import routers
from . import views 

app_name = 'carts'

router = routers.DefaultRouter()
router.register('', views.CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls)),
]