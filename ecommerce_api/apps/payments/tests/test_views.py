import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.payments.tests.factories import PaymentFactory, OrderFactory, CustomerProfileFactory
from apps.payments.models import Payment
from unittest.mock import patch
from django.core.exceptions import ValidationError

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_payment_list_view(client):
    payment = PaymentFactory()
    customer = payment.order.customer.user

    client.force_authenticate(user=customer)

    url = reverse("payments:payment-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == payment.id
    assert response.data[0]["order"] == payment.order.id
    assert response.data[0]["method"] == payment.method
    assert str(response.data[0]["amount"]) == f"{payment.amount:.2f}"
    assert response.data[0]["status"] == payment.status
    assert response.data[0]["paid_at"] == (payment.paid_at.isoformat() if payment.paid_at else None)

@pytest.mark.django_db
def test_payment_retrieve_view(client):
    payment = PaymentFactory()
    customer = payment.order.customer.user

    client.force_authenticate(user=customer)

    url = reverse("payments:payment-detail", args=[payment.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == payment.id
    assert response.data["order"] == payment.order.id
    assert response.data["method"] == payment.method
    assert str(response.data["amount"]) == f"{payment.amount:.2f}"
    assert response.data["status"] == payment.status
    assert response.data["paid_at"] == (payment.paid_at.isoformat() if payment.paid_at else None)

@pytest.mark.django_db
def test_payment_create_view(client):
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=150.00)
    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "method": "PAYPAL"
    }
    url = reverse("orders:order-payments", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["order"] == order.id
    assert response.data["method"] == "PAYPAL"
    assert str(response.data["amount"]) == "150.00"
    assert response.data["status"] == "PENDING"
    assert response.data["paid_at"] is None
    assert response.data["id"] is not None

@pytest.mark.django_db
def test_payment_create_view_unauthenticated(client):
    order = OrderFactory(total_amount=100.00)

    data = {
        "method": "CREDIT_CARD"
    }
    url = reverse("orders:order-payments", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_payment_create_view_no_order(client):
    user = CustomerProfileFactory().user

    client.force_authenticate(user=user)

    data = {
        "method": "CREDIT_CARD"
    }
    url = reverse("orders:order-payments", args=[9999])  # Non-existent order ID
    response = client.post(url, data, format='json')

    assert response.status_code == 404

@pytest.mark.django_db
def test_payment_create_view_invalid_method_for_zero_amount(client):
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=0.00)
    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "method": "CREDIT_CARD"
    }
    url = reverse("orders:order-payments", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_payment_create_view_duplicate_payment(client):
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=200.00)
    PaymentFactory(order=order)
    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "method": "PAYPAL"
    }
    url = reverse("orders:order-payments", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_payment_create_view_zero_amount_order(client):
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile, total_amount=0.00)
    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "method": "PIX"
    }
    url = reverse("orders:order-payments", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["order"] == order.id
    assert response.data["method"] == "PIX"
    assert str(response.data["amount"]) == "0.00"
    assert response.data["status"] == "PAID"
    assert response.data["paid_at"] is not None
    assert response.data["id"] is not None

@pytest.mark.django_db
def test_payment_confirm_action_payment(client):
    payment = PaymentFactory(status=Payment.Status.PENDING)
    customer = payment.order.customer.user

    client.force_authenticate(user=customer)

    url = reverse("payments:payment-confirm", args=[payment.id])
    response = client.post(url)

    assert response.status_code == 200
    assert response.data["detail"] == "Payment confirmed successfully."

    payment.refresh_from_db()
    order = payment.order
    order.refresh_from_db()

    assert payment.status == Payment.Status.PAID
    assert order.status == order.Status.CONFIRMED
    assert payment.paid_at is not None

@pytest.mark.django_db
def test_payment_confirm_action_invalid_status(client):
    payment = PaymentFactory(status=Payment.Status.PAID)
    customer = payment.order.customer.user

    client.force_authenticate(user=customer)

    url = reverse("payments:payment-confirm", args=[payment.id])
    response = client.post(url)

    assert response.status_code == 400
    assert "detail" in response.data

@pytest.mark.django_db
def test_payment_confirm_action_forbidden(client):
    payment = PaymentFactory(status=Payment.Status.PENDING)
    customer = CustomerProfileFactory().user

    client.force_authenticate(user=customer)

    url = reverse("payments:payment-confirm", args=[payment.id])
    response = client.post(url)

    assert response.status_code in [403, 404]  # Depending on whether the view checks for ownership before confirming payment
    
@pytest.mark.django_db
def test_confirm_payment_transaction_rollback():
    payment = PaymentFactory(status=Payment.Status.PENDING)
    order = payment.order

    with patch(
        'apps.payments.models.Order.mark_as_paid',
        side_effect=ValidationError("Order error")
    ):
        with pytest.raises(ValidationError):
            payment.confirm_payment()

    payment.refresh_from_db()
    order.refresh_from_db()

    assert payment.status == Payment.Status.PENDING
    assert order.payment_status == order.PaymentStatus.UNPAID
    assert payment.paid_at is None