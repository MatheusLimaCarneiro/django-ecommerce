from django.urls import path, include
from rest_framework import routers
from .views import customer
from .views.register import RegisterView

app_name = 'customers'

router = routers.DefaultRouter()
router.register('', customer.CustomerProfileViewSet, basename='customers')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]