import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.carts.models import Cart
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_cart_list_view():
    client = APIClient()

    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)
    Cart.objects.create(user=customer)

    url = reverse("carts:carts-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_cart_retrieve_view():
    client = APIClient()

    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)
    cart = Cart.objects.create(user=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == cart.id


@pytest.mark.django_db
def test_cart_create_view():
    client = APIClient()

    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)

    url = reverse("carts:carts-list")
    data = {
        "user": customer.id
    }
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["user"] == customer.id


@pytest.mark.django_db
def test_cart_update_not_allowed():
    client = APIClient()

    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)
    cart = Cart.objects.create(user=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.put(url, {"user": customer.id}, format="json")

    assert response.status_code == 405

@pytest.mark.django_db
def test_cart_delete_view():
    client = APIClient()

    user = User.objects.create_user(username="matheus", password="123")
    customer = CustomerProfile.objects.create(user=user)
    cart = Cart.objects.create(user=customer)

    url = reverse("carts:carts-detail", args=[cart.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert Cart.objects.filter(id=cart.id).count() == 0