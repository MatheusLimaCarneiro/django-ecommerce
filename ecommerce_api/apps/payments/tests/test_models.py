import pytest
from django.core.exceptions import ValidationError
from apps.payments.models import Payment
from apps.payments.tests.factories import PaymentFactory, OrderFactory

@pytest.mark.django_db
def test_create_payment():
    payment = PaymentFactory()
    assert payment.id is not None
    assert payment.amount == payment.order.total_amount
    assert payment.status == Payment.Status.PENDING

@pytest.mark.django_db
def test_payment_str():
    payment = PaymentFactory()
    expected_str = f'Payment #{payment.id} | Order #{payment.order_id} | {payment.method} | {payment.status}'
    assert str(payment) == expected_str

@pytest.mark.django_db
def test_unique_payment_per_order_constraint():
    order = OrderFactory()

    PaymentFactory(order=order)

    with pytest.raises(ValidationError) as excinfo:
        duplicate_payment = Payment(
            order=order,
            method="PAYPAL",
            amount=order.total_amount,
            status=Payment.Status.PENDING
        )
        duplicate_payment.full_clean()

    assert 'order' in excinfo.value.message_dict

@pytest.mark.django_db
def test_payment_amount_min_value():
    order = OrderFactory(total_amount=100.00)

    with pytest.raises(ValidationError) as excinfo:
        invalid_payment = Payment(
            order=order,
            method="PIX",
            amount=-50.00,
            status=Payment.Status.PENDING
        )
        invalid_payment.full_clean()

    assert 'amount' in excinfo.value.message_dict

@pytest.mark.django_db
def test_payment_amount_zero():
    order = OrderFactory(total_amount=0.00)

    payment = Payment(
        order=order,
        method="PIX",
        amount=0.00,
        status=Payment.Status.PAID
    )
    payment.full_clean()
    payment.save()

    assert payment.id is not None
    assert payment.amount == 0.00
    assert payment.status == Payment.Status.PAID

@pytest.mark.django_db
def test_payment_amount_zero_invalid_method():
    order = OrderFactory(total_amount=0.00)

    with pytest.raises(ValidationError) as excinfo:
        invalid_payment = Payment(
            order=order,
            method="CREDIT_CARD",
            amount=0.00,
            status=Payment.Status.PAID
        )
        invalid_payment.full_clean()

    assert 'method' in str(excinfo.value.message_dict)

@pytest.mark.django_db
def test_payment_factory():
    payment = PaymentFactory()
    assert isinstance(payment, Payment)
    assert payment.method in dict(Payment.Method.choices)
    assert payment.status in dict(Payment.Status.choices)