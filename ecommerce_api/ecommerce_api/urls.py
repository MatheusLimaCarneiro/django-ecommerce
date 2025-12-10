from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customers/', include('customers.urls', namespace='customers')),
    path('api/categories/', include('apps.categories.urls', namespace='categories')),
]