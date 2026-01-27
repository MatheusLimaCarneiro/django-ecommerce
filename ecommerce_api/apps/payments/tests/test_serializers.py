import pytest
from decimal import Decimal
from apps.payments.serializer import PaymentSerializer
from django.utils import timezone
from apps.payments.tests.factories import OrderFactory,CustomerProfileFactory, PaymentFactory

@pytest.mark.django_db
def test_payment_serializer():
    payment = PaymentFactory()
    serializer = PaymentSerializer(instance=payment)
    data = serializer.data

    assert data["id"] == payment.id
    assert data["order"] == payment.order.id
    assert data["method"] == payment.method
    assert str(data["amount"]) == f"{payment.amount:.2f}"
    assert data["status"] == payment.status
    assert data["paid_at"] == (payment.paid_at.isoformat() if payment.paid_at else None)
    assert data["created_at"] == timezone.localtime(payment.created_at).isoformat()

@pytest.mark.django_db
def test_payment_serializer_create():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=Decimal("100.00"))

    data = {
        "method": "CREDIT_CARD"
    }
    serializer = PaymentSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is True
    assert serializer.errors == {}
    instance = serializer.save()
    assert instance.order == order
    assert instance.method == "CREDIT_CARD"
    assert instance.amount == Decimal("100.00")
    assert instance.status == "PENDING"
    assert instance.paid_at is None
    assert instance.id is not None

@pytest.mark.django_db
def test_payment_serializer_create_zero_amount_order():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=Decimal("0.00"))

    data = {
        "method": "PIX"
    }
    serializer = PaymentSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is True
    assert serializer.errors == {}
    instance = serializer.save()
    assert instance.order == order
    assert instance.method == "PIX"
    assert instance.amount == Decimal("0.00")
    assert instance.status == "PAID"
    assert instance.paid_at is not None
    assert instance.id is not None

@pytest.mark.django_db
def test_payment_serializer_invalid_duplicate_payment():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=Decimal("50.00"))

    PaymentFactory(order=order)

    data = {
        "method": "PAYPAL"
    }
    serializer = PaymentSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_payment_serializer_invalid_zero_amount_method():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=Decimal("0.00"))

    data = {
        "method": "CREDIT_CARD"
    }
    serializer = PaymentSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_payment_serializer_missing_order_in_context():
    data = {
        "method": "PIX"
    }
    serializer = PaymentSerializer(data=data, context={})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_payment_serializer_creates_payment_without_order_in_payload():
    order = OrderFactory(total_amount=Decimal("20.00"))

    data = {
        "method": "PIX"
    }
    serializer = PaymentSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.order == order