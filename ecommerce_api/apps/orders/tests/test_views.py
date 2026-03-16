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

    client.force_authenticate(user=order.customer.user)

    url = reverse("orders:order-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == order.id
    assert response.data[0]["customer"] == order.customer.id

@pytest.mark.django_db
def test_order_retrieve_view(client):
    order = OrderFactory()

    client.force_authenticate(user=order.customer.user)

    url = reverse("orders:order-detail", args=[order.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == order.id

    assert response.data["customer"] == order.customer.id
    assert response.data["status"] == order.status
    assert response.data["payment_status"] == order.payment_status
    assert str(response.data["total_amount"]) == f"{order.total_amount:.2f}"

@pytest.mark.django_db
def test_order_create_view_unauthenticated(client):
    url = reverse("orders:order-list")
    response = client.post( url, {}, format='json')

    assert response.status_code == 401
    assert "detail" in response.data
    
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