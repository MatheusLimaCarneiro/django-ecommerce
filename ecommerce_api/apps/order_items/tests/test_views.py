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
    order_item = OrderItemFactory()

    url = reverse("order_items:orderitem-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == order_item.id
    assert response.data[0]["order"] == order_item.order.id
    assert response.data[0]["product"] == order_item.product.id
    assert response.data[0]["quantity"] == order_item.quantity
    assert str(response.data[0]["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(response.data[0]["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_retrieve_view(client):
    order_item = OrderItemFactory()

    url = reverse("order_items:orderitem-detail", args=[order_item.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == order_item.id
    assert response.data["order"] == order_item.order.id
    assert response.data["product"] == order_item.product.id
    assert response.data["quantity"] == order_item.quantity
    assert str(response.data["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(response.data["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_create_view(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)
    product = ProductFactory(stock=10, price=Decimal("15.00"))

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 2
    }
    url = reverse("order_items:orderitem-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["order"] == order.id
    assert response.data["product"] == product.id
    assert response.data["quantity"] == 2
    assert str(response.data["unit_price"]) == "15.00"
    assert str(response.data["subtotal"]) == "30.00"

@pytest.mark.django_db
def test_order_item_create_view_unauthenticated(client):
    order = OrderFactory()
    product = ProductFactory(stock=10, price=Decimal("15.00"))

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 2
    }
    url = reverse("order_items:orderitem-list")
    response = client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_order_item_create_view_invalid_product_inactive(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer = customer_profile)
    product = ProductFactory(is_active=False)

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 1
    }
    url = reverse("order_items:orderitem-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_order_item_create_view_invalid_product_out_of_stock(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)
    product = ProductFactory(stock=0)

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 1
    }
    url = reverse("order_items:orderitem-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_order_item_create_view_invalid_quantity_exceeds_stock(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)
    product = ProductFactory(stock=5)

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 10  # Exceeds available stock
    }
    url = reverse("order_items:orderitem-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_order_item_create_view_invalid_quantity_zero(client):
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)
    product = ProductFactory(stock=10)

    data = {
        "order": order.id,
        "product": product.id,
        "quantity": 0  # Invalid quantity
    }
    url = reverse("order_items:orderitem-list")
    client.force_authenticate(user=user)
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "quantity" in response.data

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