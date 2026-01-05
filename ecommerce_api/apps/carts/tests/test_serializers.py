import pytest
from apps.carts.models import Cart
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User
from apps.carts.serializer import CartSerializer

@pytest.mark.django_db
def test_cart_serializer():
    user = User.objects.create_user(username="matheus", password="123")

    customer = CustomerProfile.objects.create(user=user)

    cart = Cart.objects.create(user = customer)

    serializer = CartSerializer(cart)
    data = serializer.data

    assert data["id"] == cart.id
    assert data["user"] == customer.id
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.django_db
def test_cart_serializer_create():
    user = User.objects.create_user(username="matheus", password="123")
    
    customer = CustomerProfile.objects.create(user=user)
    
    data = {
        "user": customer.id
    }

    serializer = CartSerializer(data=data)
    assert serializer.is_valid() is True
    
    instance = serializer.save()
    assert instance.user == customer
    assert instance.id is not None
    assert instance.created_at is not None


@pytest.mark.django_db
def test_invalid_cart_serializer():
    data = {
        "user": None
    }

    serializer = CartSerializer(data=data)
    assert serializer.is_valid() is False
    assert "user" in serializer.errors