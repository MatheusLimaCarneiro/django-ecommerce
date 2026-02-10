import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.orders.models import Order
from apps.orders.tests.factories import OrderFactory, CustomerProfileFactory, UserFactory, ProductFactory
from decimal import Decimal

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_order_list_view(client):
    order = OrderFactory()

    url = reverse("orders:order-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == order.id
    assert response.data[0]["customer"] == order.customer.id

@pytest.mark.django_db
def test_order_retrieve_view(client):
    order = OrderFactory()

    url = reverse("orders:order-detail", args=[order.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == order.id

    assert response.data["customer"] == order.customer.id
    assert response.data["status"] == order.status
    assert response.data["payment_status"] == order.payment_status
    assert str(response.data["total_amount"]) == f"{order.total_amount:.2f}"

@pytest.mark.django_db
def test_order_create_view(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)

    data = {
        "status": "PENDING",
        "payment_status": "UNPAID",
    }
    url = reverse("orders:order-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["customer"] == customer_profile.id
    assert response.data["status"] == "PENDING"
    assert response.data["payment_status"] == "UNPAID"
    assert str(response.data["total_amount"]) == "0.00"

@pytest.mark.django_db
def test_order_create_view_unauthenticated(client):
    url = reverse("orders:order-list")
    response = client.post( url, {}, format='json')

    assert response.status_code == 401
    assert "detail" in response.data

@pytest.mark.django_db
def test_order_create_view_no_customer_profile(client):
    user = UserFactory()

    url = reverse("orders:order-list")
    client.force_authenticate(user=user)
    response = client.post(url, {}, format='json')

    assert response.status_code == 400
    assert "customer" in response.data

@pytest.mark.django_db
def test_order_update_view_not_allowed(client):
    order = OrderFactory()
    customer = order.customer

    client.force_authenticate(user=customer.user)
    url = reverse("orders:order-detail", args=[order.id])
    
    response = client.put(url, {}, format='json')
    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_order_delete_view_not_allowed(client):
    order = OrderFactory()
    customer = order.customer

    client.force_authenticate(user=customer.user)
    url = reverse("orders:order-detail", args=[order.id])
    response = client.delete(url)

    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_add_item_success(client):
    customer = CustomerProfileFactory()
    order = OrderFactory(customer=customer, status=Order.Status.PENDING, payment_status=Order.PaymentStatus.UNPAID)
    product = ProductFactory(stock=10, price=Decimal("20.00"))

    client.force_authenticate(user=customer.user)

    data = {
        "product": product.id,
        "quantity": 2
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["product"] == product.id
    assert response.data["quantity"] == 2
    assert str(response.data["unit_price"]) == "20.00"
    assert str(response.data["subtotal"]) == "40.00"

@pytest.mark.django_db
def test_add_item_forbidden_other_user(client):
    customer1 = CustomerProfileFactory()
    customer2 = CustomerProfileFactory()
    order = OrderFactory(customer=customer1, status=Order.Status.PENDING, payment_status=Order.PaymentStatus.UNPAID)
    product = ProductFactory(stock=10, price=Decimal("20.00"))

    client.force_authenticate(user=customer2.user)

    data = {
        "product": product.id,
        "quantity": 2
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 403
    assert "detail" in response.data

@pytest.mark.django_db
def test_add_item_order_not_pending(client):
    customer = CustomerProfileFactory()
    order = OrderFactory(customer=customer, status=Order.Status.CONFIRMED, payment_status=Order.PaymentStatus.UNPAID)
    product = ProductFactory(stock=10, price=Decimal("20.00"))

    client.force_authenticate(user=customer.user)

    data = {
        "product": product.id,
        "quantity": 2
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "detail" in response.data

@pytest.mark.django_db
def test_add_item_paid_order(client):
    customer = CustomerProfileFactory()
    order = OrderFactory(customer=customer, status=Order.Status.PENDING, payment_status=Order.PaymentStatus.PAID)
    product = ProductFactory(stock=10, price=Decimal("20.00"))

    client.force_authenticate(user=customer.user)

    data = {
        "product": product.id,
        "quantity": 2
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "detail" in response.data

@pytest.mark.django_db
def test_add_item_invalid_product(client):
    customer = CustomerProfileFactory()
    order = OrderFactory(customer=customer, status=Order.Status.PENDING, payment_status=Order.PaymentStatus.UNPAID)

    client.force_authenticate(user=customer.user)

    data = {
        "product": 9999,  # Non-existent product ID
        "quantity": 2
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "product" in response.data

@pytest.mark.django_db
def test_add_item_invalid_quantity(client):
    customer = CustomerProfileFactory()
    order = OrderFactory(customer=customer, status=Order.Status.PENDING, payment_status=Order.PaymentStatus.UNPAID)
    product = ProductFactory(stock=10, price=Decimal("20.00"))

    client.force_authenticate(user=customer.user)

    data = {
        "product": product.id,
        "quantity": -1  # Invalid quantity
    }
    url = reverse("orders:order-item", args=[order.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "quantity" in response.data