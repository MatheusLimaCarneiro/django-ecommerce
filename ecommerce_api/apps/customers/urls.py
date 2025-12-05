from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'customers'

router = routers.DefaultRouter()
router.register('', views.CustomerProfileViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
]