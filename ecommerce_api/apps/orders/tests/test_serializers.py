import pytest
from apps.orders.tests.factories import OrderFactory, CustomerProfileFactory, UserFactory
from rest_framework.test import APIRequestFactory
from apps.orders.serializer import OrderSerializer
from decimal import Decimal
from rest_framework import serializers

@pytest.mark.django_db
def test_order_serializer():
    order = OrderFactory()
    serializer = OrderSerializer(instance=order)
    data = serializer.data

    assert data["id"] == order.id
    assert data["customer"] == order.customer.id
    assert data["status"] == order.status
    assert data["payment_status"] == order.payment_status
    assert Decimal(data["total_amount"]) == order.total_amount

@pytest.mark.django_db
def test_order_serializer_create():
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)

    factory = APIRequestFactory()
    request = factory.post("/orders/")
    request.user = user

    serializer = OrderSerializer(data={}, context={"request": request})
    assert serializer.is_valid()

    order = serializer.save()

    assert order.customer == customer_profile
    assert order.status == "PENDING"
    assert order.payment_status == "UNPAID"
    assert order.total_amount == Decimal("0.00")

@pytest.mark.django_db
def test_order_serializer_create_without_customer_profile():
    user = UserFactory()

    factory = APIRequestFactory()
    request = factory.post("/orders/")
    request.user = user

    serializer = OrderSerializer(data={}, context={"request": request})
    assert serializer.is_valid()

    with pytest.raises(serializers.ValidationError) as exc:
        serializer.save()

    error = exc.value.detail
    assert "customer" in error

@pytest.mark.django_db
def test_order_serializer_create_without_authentication():
    factory = APIRequestFactory()
    request = factory.post("/orders/")
    request.user = None

    serializer = OrderSerializer(data={}, context={"request": request})
    assert serializer.is_valid()

    with pytest.raises(serializers.ValidationError) as exc:
        serializer.save()

    error = exc.value.detail
    assert "user" in error