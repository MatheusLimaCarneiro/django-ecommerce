import pytest
from apps.carts.models import Cart
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_create_cart():
    user = User.objects.create_user(username="matheus", password="123")

    customer = CustomerProfile.objects.create(user=user)

    cart = Cart.objects.create(user = customer)

    assert cart.user == customer
    assert cart.id is not None
    assert cart.created_at is not None


@pytest.mark.django_db
def test_cart_str():
    user = User.objects.create_user(username="matheus", password="123")

    customer = CustomerProfile.objects.create(user=user)

    cart = Cart.objects.create(user = customer)

    expected_str = "Cart of {}".format(customer)

    assert str(cart) == expected_str


@pytest.mark.django_db
def test_cart_ordering():
    user1 = User.objects.create_user(username="u1", password="123")
    user2 = User.objects.create_user(username="u2", password="123")

    customer1 = CustomerProfile.objects.create(user=user1)
    customer2 = CustomerProfile.objects.create(user=user2)

    cart1 = Cart.objects.create(user=customer1)
    cart2 = Cart.objects.create(user=customer2)

    carts = Cart.objects.all()
    assert list(carts) == [cart1, cart2]


@pytest.mark.django_db
def test_user_can_have_only_one_cart():
    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    Cart.objects.create(user=customer)

    with pytest.raises(IntegrityError):
        Cart.objects.create(user=customer)