import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products.models import Product
from apps.categories.models import Category
from decimal import Decimal


@pytest.mark.django_db
def test_product_list_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    Product.objects.create(
        name="Smartphone",
        category=category,
        description="An advanced smartphone",
        price=1999.99,
        stock=10,
        is_active=True
    )

    url = reverse("products:products-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_product_retrieve_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Laptop",
        category=category,
        description="A powerful laptop",
        price=2999.99,
        stock=5,
        is_active=True
    )

    url = reverse("products:products-detail", args=[product.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == "Laptop"


@pytest.mark.django_db
def test_product_create_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")

    url = reverse("products:products-list")
    data = {
        "name": "Tablet",
        "category": category.id,
        "description": "A versatile tablet",
        "price": 999.99,
        "stock": 20,
        "is_active": True
    }

    response = client.post(url, data)
    assert response.status_code == 201
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_product_update_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Smartwatch",
        category=category,
        description="A modern smartwatch",
        price=499.99,
        stock=15,
        is_active=True
    )

    url = reverse("products:products-detail", args=[product.id])
    data = {
        "name": "Updated Smartwatch",
        "category": category.id,
        "description": "An even more modern smartwatch",
        "price": 599.99,
        "stock": 10,
        "is_active": True
    }

    response = client.put(url, data)
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Updated Smartwatch"
    assert product.price == Decimal("599.99")


@pytest.mark.django_db
def test_product_partial_update_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Headphones",
        category=category,
        description="Noise cancelling headphones",
        price=299.99,
        stock=25,
        is_active=True
    )

    url = reverse("products:products-detail", args=[product.id])
    data = {"price": 249.99}

    response = client.patch(url, data)
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.price == Decimal("249.99")


@pytest.mark.django_db
def test_product_delete_view():
    client = APIClient()

    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Camera",
        category=category,
        description="High resolution digital camera",
        price=1499.99,
        stock=8,
        is_active=True
    )

    url = reverse("products:products-detail", args=[product.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert Product.objects.count() == 0