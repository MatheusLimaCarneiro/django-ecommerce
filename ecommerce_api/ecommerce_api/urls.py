from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/customers/', include('apps.customers.urls', namespace='customers')),
    path('api/categories/', include('apps.categories.urls', namespace='categories')),
    path('api/products/', include('apps.products.urls', namespace='products')),
    path('api/carts/', include('apps.carts.urls', namespace='carts')),
    path('api/cart-items/', include('apps.cart_items.urls', namespace='cart_items')),
    path('api/orders/', include('apps.orders.urls', namespace='orders')),
    path('api/order-items/', include('apps.order_items.urls', namespace='order_items')),
    path('api/payments/', include('apps.payments.urls', namespace='payments')),
    path('api/reviews/', include('apps.reviews.urls', namespace='reviews')),

]