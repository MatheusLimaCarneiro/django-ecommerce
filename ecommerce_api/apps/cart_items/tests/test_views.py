import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.cart_items.models import CartItem
from apps.cart_items.tests.factories import CartItemFactory, ProductFactory, CartFactory

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_cart_item_list_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)

    url = reverse("cart_items:cart-item-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == cart_item.id
    assert response.data[0]["cart"] == cart_item.cart.id

@pytest.mark.django_db
def test_cart_item_retrieve_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)

    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == cart_item.id

    assert response.data["cart"] == cart_item.cart.id
    assert response.data["product"] == cart_item.product.id

@pytest.mark.django_db
def test_cart_item_create_view(client):
    cart = CartFactory()
    product = ProductFactory(stock=10)

    data = {
        "cart": cart.id,
        "product": product.id,
        "quantity": 3,
        "price_at_time": "10.00"
    }

    client.force_authenticate(user=cart.user.user)

    url = reverse("cart_items:cart-item-list")
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["cart"] == cart.id
    assert response.data["product"] == product.id
    assert response.data["quantity"] == 3
    assert str(response.data["price_at_time"]) == "10.00"

@pytest.mark.django_db
def test_cart_item_update_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "cart": cart_item.cart.id,
        "product": cart_item.product.id,
        "quantity": 5,
        "price_at_time": "10.00"
    }

    response = client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data["quantity"] == 5

@pytest.mark.django_db
def test_cart_item_delete_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert CartItem.objects.filter(id=cart_item.id).count() == 0

@pytest.mark.django_db
def test_cart_item_partial_update_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)

    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "quantity": 4
    }
    response = client.patch(url, data, format='json')

    assert response.status_code == 200
    assert response.data["quantity"] == 4

@pytest.mark.django_db
def test_cart_item_create_exceeding_stock(client):
    cart = CartFactory()
    product = ProductFactory(stock=5)

    data = {
        "cart": cart.id,
        "product": product.id,
        "quantity": 10,
        "price_at_time": "10.00"
    }

    client.force_authenticate(user=cart.user.user)

    url = reverse("cart_items:cart-item-list")
    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)

@pytest.mark.django_db
def test_cart_item_update_exceeding_stock(client):
    cart_item = CartItemFactory()

    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "cart": cart_item.cart.id,
        "product": cart_item.product.id,
        "quantity": 104,
        "price_at_time": "10.00"
    }

    client.force_authenticate(user=cart_item.cart.user.user)

    response = client.put(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)

@pytest.mark.django_db
def test_cart_item_partial_update_exceeding_stock(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.user.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "quantity": 104
    }

    response = client.patch(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)