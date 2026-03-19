import pytest
from apps.carts.models import Cart
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User
from apps.carts.serializer import CartSerializer

@pytest.mark.django_db
def test_cart_serializer():
    user = User.objects.create_user(username="matheus", password="123")

    customer = CustomerProfile.objects.create(user=user)

    cart = Cart.objects.create(customer = customer)

    serializer = CartSerializer(cart)
    data = serializer.data

    assert data["id"] == cart.id
    assert "created_at" in data
    assert "updated_at" in data