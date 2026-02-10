import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.order_items.tests.factories import OrderItemFactory, OrderFactory, ProductFactory, CustomerProfileFactory, UserFactory
from decimal import Decimal

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_order_item_list_view(client):
    customer = CustomerProfileFactory()
    order_item = OrderItemFactory(order__customer=customer)

    client.force_authenticate(user=customer.user)

    url = reverse("order_items:orderitem-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == order_item.id
    assert response.data[0]["product"] == order_item.product.id
    assert response.data[0]["quantity"] == order_item.quantity
    assert str(response.data[0]["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(response.data[0]["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_retrieve_view(client):
    customer = CustomerProfileFactory()
    order_item = OrderItemFactory(order__customer=customer)

    client.force_authenticate(user=customer.user)

    url = reverse("order_items:orderitem-detail", args=[order_item.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == order_item.id
    assert response.data["product"] == order_item.product.id
    assert response.data["quantity"] == order_item.quantity
    assert str(response.data["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(response.data["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_update_view_not_allowed(client):
    user = UserFactory()
    client.force_authenticate(user=user)
    order_item = OrderItemFactory()
    data = {
        "quantity": 5
    }
    url = reverse("order_items:orderitem-detail", args=[order_item.id])
    response = client.put(url, data, format='json')

    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_order_item_delete_view_not_allowed(client):
    user = UserFactory()
    client.force_authenticate(user=user)
    order_item = OrderItemFactory()

    url = reverse("order_items:orderitem-detail", args=[order_item.id])
    response = client.delete(url)

    assert response.status_code == 405  # Method Not Allowed