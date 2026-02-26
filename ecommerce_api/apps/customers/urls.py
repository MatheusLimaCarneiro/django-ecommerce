from django.urls import path, include
from rest_framework import routers
from . import views
from .registerView import RegisterView

app_name = 'customers'

router = routers.DefaultRouter()
router.register('', views.CustomerProfileViewSet, basename='customers')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]