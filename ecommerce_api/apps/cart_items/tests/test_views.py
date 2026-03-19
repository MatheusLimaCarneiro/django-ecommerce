import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.cart_items.models import CartItem
from apps.cart_items.tests.factories import CartItemFactory, ProductFactory, CartFactory, CustomerProfileFactory
from apps.carts.models import Cart

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_cart_item_list_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)

    url = reverse("cart_items:cart-item-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == cart_item.id
    assert response.data[0]["product"] == cart_item.product.id
    assert response.data[0]["quantity"] == cart_item.quantity
    assert str(response.data[0]["price_at_time"]) == f"{cart_item.price_at_time:.2f}"

@pytest.mark.django_db
def test_cart_item_retrieve_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)

    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == cart_item.id
    assert response.data["product"] == cart_item.product.id
    assert response.data["quantity"] == cart_item.quantity
    assert str(response.data["price_at_time"]) == f"{cart_item.price_at_time:.2f}"

@pytest.mark.django_db
def test_cart_item_create_view(client):
    cart = CartFactory()
    product = ProductFactory(stock=10)

    data = {
        "product": product.id,
        "quantity": 3,
    }

    client.force_authenticate(user=cart.customer.user)

    url = reverse("cart_items:cart-item-list")
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["product"] == product.id
    assert response.data["quantity"] == 3
    assert str(response.data["price_at_time"]) == "10.00"

@pytest.mark.django_db
def test_cart_item_update_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "product": cart_item.product.id,
        "quantity": 5,
    }

    response = client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data["quantity"] == 5

@pytest.mark.django_db
def test_cart_item_delete_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert CartItem.objects.filter(id=cart_item.id).count() == 0

@pytest.mark.django_db
def test_cart_item_partial_update_view(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)

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
        "product": product.id,
        "quantity": 10,
    }

    client.force_authenticate(user=cart.customer.user)

    url = reverse("cart_items:cart-item-list")
    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)

@pytest.mark.django_db
def test_cart_item_update_exceeding_stock(client):
    cart_item = CartItemFactory()

    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "product": cart_item.product.id,
        "quantity": 104,
    }

    client.force_authenticate(user=cart_item.cart.customer.user)

    response = client.put(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)

@pytest.mark.django_db
def test_cart_item_partial_update_exceeding_stock(client):
    cart_item = CartItemFactory()

    client.force_authenticate(user=cart_item.cart.customer.user)
    
    url = reverse("cart_items:cart-item-detail", args=[cart_item.id])
    data = {
        "quantity": 104
    }

    response = client.patch(url, data, format='json')
    assert response.status_code == 400
    assert "Requested quantity exceeds available stock." in str(response.data)

@pytest.mark.django_db
def test_cart_is_created_when_adding_first_item(client):
    customer = CustomerProfileFactory()
    product = ProductFactory(stock=10)

    client.force_authenticate(user=customer.user)

    url = reverse("cart_items:cart-item-list")

    data = {
        "product": product.id,
        "quantity": 2,
    }

    assert Cart.objects.filter(customer=customer).count() == 0

    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert Cart.objects.filter(customer=customer).count() == 1

@pytest.mark.django_db
def test_cart_item_is_not_duplicated_when_adding_same_product(client):
    cart_item = CartItemFactory(quantity=2)

    client.force_authenticate(user=cart_item.cart.customer.user)

    url = reverse("cart_items:cart-item-list")

    data = {
        "product": cart_item.product.id,
        "quantity": 3,
    }

    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert CartItem.objects.filter(cart=cart_item.cart, product=cart_item.product).count() == 1

    updated_cart_item = CartItem.objects.get(cart=cart_item.cart, product=cart_item.product)
    assert updated_cart_item.quantity == 5  # Original 2 + New 3

@pytest.mark.django_db
def test_cannot_add_inactive_product(client):
    customer = CustomerProfileFactory()
    product = ProductFactory(is_active=False)

    client.force_authenticate(user=customer.user)

    url = reverse("cart_items:cart-item-list")

    data = {
        "product": product.id,
        "quantity": 1
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert "inactive" in str(response.data)