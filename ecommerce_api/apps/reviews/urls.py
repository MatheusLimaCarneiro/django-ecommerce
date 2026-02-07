from django.urls import path, include
from rest_framework import routers
from . import views 

app_name = 'reviews'

router = routers.DefaultRouter()
router.register('', views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]