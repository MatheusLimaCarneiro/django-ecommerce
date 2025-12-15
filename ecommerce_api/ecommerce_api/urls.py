from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customers/', include('apps.customers.urls', namespace='customers')),
    path('api/categories/', include('apps.categories.urls', namespace='categories')),
    path('api/products/', include('apps.products.urls', namespace='products')),
]