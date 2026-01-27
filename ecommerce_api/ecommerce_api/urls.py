from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customers/', include('apps.customers.urls', namespace='customers')),
    path('api/categories/', include('apps.categories.urls', namespace='categories')),
    path('api/products/', include('apps.products.urls', namespace='products')),
    path('api/carts/', include('apps.carts.urls', namespace='carts')),
    path('api/cart-items/', include('apps.cart_items.urls', namespace='cart_items')),
    path('api/orders/', include('apps.orders.urls', namespace='orders')),
    path('api/order-items/', include('apps.order_items.urls', namespace='order_items')),
    path('api/payments/', include('apps.payments.urls', namespace='payments')),

]