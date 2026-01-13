import pytest
from apps.orders.tests.factories import OrderFactory, CustomerProfileFactory, UserFactory
from apps.orders.serializer import OrderSerializer
from decimal import Decimal
from rest_framework import serializers

@pytest.mark.django_db
def test_order_serializer():
    order = OrderFactory()
    serializer = OrderSerializer(instance=order)
    data = serializer.data

    assert data["id"] == order.id
    assert data["customer"]["id"] == order.customer.id
    assert data["status"] == order.status
    assert data["payment_status"] == order.payment_status
    assert str(data["total_amount"]) == f"{order.total_amount:.2f}"

@pytest.mark.django_db
def test_order_serializer_create():
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)

    data = {
        "status": "PENDING",
        "payment_status": "UNPAID",
    }
    context = {"request": type('Request', (object,), {'user': user})()}
    serializer = OrderSerializer(data=data, context=context)
    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.customer == customer_profile
    assert instance.status == "PENDING"
    assert instance.payment_status == "UNPAID"
    assert instance.total_amount == Decimal("0.00")
    assert instance.id is not None

@pytest.mark.django_db
def test_order_serializer_invalid_create():
    user = UserFactory()
    data = {
        "status": "INVALID_STATUS",  # Invalid status
        "payment_status": "UNPAID",
    }
    context = {"request": type('Request', (object,), {'user': user})()}
    serializer = OrderSerializer(data=data, context=context)
    assert serializer.is_valid() is True  # Serializer allows any string for status
    assert serializer.validated_data == {}

@pytest.mark.django_db
def test_order_serializer_read_only_fields():
    order = OrderFactory(status="SHIPPED", payment_status="PAID", total_amount=100.00)
    serializer = OrderSerializer(instance=order)
    data = serializer.data

    assert data["status"] == "SHIPPED"
    assert data["payment_status"] == "PAID"
    assert str(data["total_amount"]) == "100.00"

@pytest.mark.django_db
def test_order_serializer_create_without_customer_profile():
    user = UserFactory()

    data = {
        "status": "PENDING",
        "payment_status": "UNPAID",
    }
    context = {"request": type('Request', (object,), {'user': user})()}
    serializer = OrderSerializer(data=data, context=context)
    assert serializer.is_valid() is True
    assert serializer.validated_data == {}
    with pytest.raises(serializers.ValidationError) as excinfo:
        serializer.save()
    assert "Customer profile not found for this user." in str(excinfo.value)

@pytest.mark.django_db
def test_order_serializer_create_without_authentication():
    data = {
        "status": "PENDING",
        "payment_status": "UNPAID",
    }
    context = {"request": type('Request', (object,), {'user': None})()}
    serializer = OrderSerializer(data=data, context=context)
    assert serializer.is_valid() is True
    assert serializer.validated_data == {}
    with pytest.raises(serializers.ValidationError) as excinfo:
        serializer.save()
    assert "Authentication required to create an order." in str(excinfo.value)