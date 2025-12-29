import pytest
from apps.products.models import Product
from apps.categories.models import Category
from apps.products.serializer import ProductSerializer
from decimal import Decimal


@pytest.mark.django_db
def test_product_serializer():
    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Tablet",
        category=category,
        description="A versatile tablet",
        price=999.99,
        stock=20,
        is_active=True
    )

    serializer = ProductSerializer(product)
    data = serializer.data

    assert data["name"] == "Tablet"
    assert data["category"] == category.id
    assert data["description"] == "A versatile tablet"
    assert float(data["price"]) == 999.99
    assert data["stock"] == 20
    assert data["is_active"] is True
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.django_db
def test_product_serializer_create():
    category = Category.objects.create(name="Electronics")

    data = {
        "name": "Smartwatch",
        "category": category.id,
        "description": "A modern smartwatch",
        "price": 499.99,
        "stock": 15,
        "is_active": True
    }

    serializer = ProductSerializer(data=data)
    assert serializer.is_valid() is True

    instance = serializer.save()
    assert instance.name == "Smartwatch"
    assert instance.category == category
    assert instance.description == "A modern smartwatch"
    assert instance.price == Decimal("499.99")
    assert instance.stock == 15
    assert instance.is_active is True


@pytest.mark.django_db
def test_invalid_product_serializer():
    data = {
        "name": "",
        "category": None,
        "description": "Invalid description",
        "price": -100.00,
        "stock": -5,
        "is_active": True
    }

    serializer = ProductSerializer(data=data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors
    assert "category" in serializer.errors
    assert "price" in serializer.errors
    assert "stock" in serializer.errors