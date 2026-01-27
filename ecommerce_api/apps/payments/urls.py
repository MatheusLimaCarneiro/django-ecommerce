from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'payments'

router = routers.DefaultRouter()
router.register('', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('payments/', include(router.urls)),
]