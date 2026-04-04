import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.carts.models import Cart
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User
from apps.carts.tests.factories import CartFactory, CustomerProfileFactory, UserFactory, CategoryFactory, ProductFactory, CartItemFactory
from apps.orders.models import Order
from apps.order_items.models import OrderItem

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_cart_list_view(client):
    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart =Cart.objects.create(customer=customer)

    url = reverse("carts:carts-list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == cart.id


@pytest.mark.django_db
def test_cart_retrieve_view(client):
    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)
    
    cart = Cart.objects.create(customer=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == cart.id


@pytest.mark.django_db
def test_cart_update_not_allowed(client):
    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.put(url, {"customer": customer.id}, format="json")

    assert response.status_code == 405

@pytest.mark.django_db
def test_cart_delete_view(client):
    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert Cart.objects.filter(id=cart.id).count() == 0
    
@pytest.mark.django_db
def test_cart_checkout(client):
    user = UserFactory()
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    category = CategoryFactory()
    product = ProductFactory(category=category)
    cart_item = CartItemFactory(cart=cart, product=product)

    url = reverse("carts:carts-checkout", args=[cart.id])
    response = client.post(url)

    assert response.status_code == 201
    assert response.data["customer"] == customer.id
    
    assert Order.objects.count() == 1

    order = Order.objects.first()
    assert order.customer == customer

    assert OrderItem.objects.count() == 1
    order_item = OrderItem.objects.first()
    assert order_item.order == order
    assert order_item.product == product
    assert order_item.quantity == cart_item.quantity
    assert order_item.unit_price == cart_item.price_at_time
    assert order_item.subtotal == cart_item.price_at_time * cart_item.quantity
    
    assert cart.items.count() == 0

@pytest.mark.django_db
def test_cart_checkout_multiple_items(client):
    user = UserFactory()
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    category = CategoryFactory()
    product1 = ProductFactory(category=category)
    product2 = ProductFactory(category=category)

    cart_item1 = CartItemFactory(cart=cart, product=product1)
    cart_item2 = CartItemFactory(cart=cart, product=product2)

    url = reverse("carts:carts-checkout", args=[cart.id])
    response = client.post(url)

    assert response.status_code == 201
    assert response.data["customer"] == customer.id
    
    assert Order.objects.count() == 1

    order = Order.objects.first()
    assert order.customer == customer

    assert OrderItem.objects.count() == 2

@pytest.mark.django_db
def test_user_cannot_access_other_user_cart(client):
    user1 = UserFactory()
    user2 = UserFactory()

    customer1 = CustomerProfileFactory(user=user1)
    customer2 = CustomerProfileFactory(user=user2)

    cart = CartFactory(customer=customer1)

    client.force_authenticate(user=user2)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_checkout_empty_cart(client):
    user = UserFactory()
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    url = reverse("carts:carts-checkout", args=[cart.id])
    response = client.post(url)

    assert response.status_code == 400
    assert response.data["detail"] == "Cannot checkout an empty cart."

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0

@pytest.mark.django_db
def test_checkout_insufficient_stock(client):
    user = UserFactory()
    customer = CustomerProfile.objects.create(user=user)

    client.force_authenticate(user=user)

    cart = Cart.objects.create(customer=customer)

    category = CategoryFactory()
    product = ProductFactory(category=category, stock=1)
    cart_item = CartItemFactory(cart=cart, product=product, quantity=2)

    url = reverse("carts:carts-checkout", args=[cart.id])
    response = client.post(url)

    assert response.status_code == 400
    assert response.data["detail"] == f"Not enough stock for product '{product.name}'"

    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0