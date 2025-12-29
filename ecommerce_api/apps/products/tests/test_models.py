import pytest
from apps.products.models import Product
from apps.categories.models import Category
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_create_product():
    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Smartphone",
        category=category,
        description="A modern smartphone",
        price=1999.99,
        stock=50,
        is_active=True
    )

    assert product.name == "Smartphone"
    assert product.category.name == "Electronics"
    assert product.description == "A modern smartphone"
    assert product.price == 1999.99
    assert product.stock == 50
    assert product.is_active is True


@pytest.mark.django_db
def test_product_str():
    category = Category.objects.create(name="Electronics")
    product = Product.objects.create(
        name="Laptop",
        category=category,
        description="A powerful laptop",
        price=2999.99,
        stock=30,
        is_active=True
    )

    assert str(product) == "Laptop"


@pytest.mark.django_db
def test_product_ordering():
    category = Category.objects.create(name="Electronics")

    p1 = Product.objects.create(
        name="Product A",
        category=category,
        description="Description A",
        price=100.00,
        stock=10,
        is_active=True
    )
    p2 = Product.objects.create(
        name="Product B",
        category=category,
        description="Description B",
        price=200.00,
        stock=20,
        is_active=True
    )

    products = Product.objects.all()
    assert list(products) == [p1, p2]


@pytest.mark.django_db
def test_product_negative_price_not_allowed():
    category = Category.objects.create(name="Electronics")

    product = Product(
        name="Invalid product",
        category=category,
        price=-10,
        stock=5
    )

    with pytest.raises(ValidationError):
        product.full_clean()


@pytest.mark.django_db
def test_product_negative_stock_not_allowed():
    category = Category.objects.create(name="Electronics")

    product = Product(
        name="Invalid product",
        category=category,
        price=100,
        stock=-5
    )

    with pytest.raises(ValidationError):
        product.full_clean()