import pytest
from apps.cart_items.serializer import CartItemSerializer
from decimal import Decimal
from rest_framework import serializers
from apps.cart_items.tests.factories import CartItemFactory, ProductFactory, CartFactory
@pytest.mark.django_db
def test_cart_item_serializer():
    cart_item = CartItemFactory()
    serializer = CartItemSerializer(instance=cart_item)
    data = serializer.data

    assert data["id"] == cart_item.id
    assert data["cart"] == cart_item.cart.id
    assert data["product"] == cart_item.product.id
    assert data["quantity"] == cart_item.quantity
    assert str(data["price_at_time"]) == f"{cart_item.price_at_time:.2f}"

@pytest.mark.django_db
def test_cart_item_serializer_create():
    cart = CartFactory()
    product = ProductFactory(stock=10)

    data = {
        "cart": cart.id,
        "product": product.id,
        "quantity": 3,
        "price_at_time": "10.00"
    }
    serializer = CartItemSerializer(data=data)
    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.cart == cart
    assert instance.product == product
    assert instance.quantity == 3
    assert instance.price_at_time == Decimal("10.00")
    assert instance.id is not None

@pytest.mark.django_db
def test_invalid_cart_item_serializer():
    cart = CartFactory()
    prdouct = ProductFactory(stock=2)

    data = {
        "cart": cart.id,
        "product": prdouct.id,
        "quantity": 5,  # Exceeds stock
        "price_at_time": "10.00"
    }
    serializer = CartItemSerializer(data=data)
    assert serializer.is_valid() is False
    assert "Requested quantity exceeds available stock." in str(serializer.errors)

@pytest.mark.django_db
def test_cart_item_serializer_create_existing_item():
    cart_item = CartItemFactory(quantity=2)
    cart = cart_item.cart
    product = cart_item.product

    data = {
        "cart": cart.id,
        "product": product.id,
        "quantity": 3,  # Adding more quantity
        "price_at_time": "10.00"
    }

    serializer = CartItemSerializer(data=data)

    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.cart == cart
    assert instance.product == product
    assert instance.quantity == 5  # 2 + 3
    assert instance.price_at_time == Decimal("10.00")
    assert instance.id == cart_item.id

@pytest.mark.django_db
def test_cart_item_serializer_create_existing_item_exceeds_stock():
    cart_item = CartItemFactory(quantity=3, product__stock=6)
    cart = cart_item.cart
    product = cart_item.product

    data = {
        "cart": cart.id,
        "product": product.id,
        "quantity": 4,  # 3 + 4 > 6
        "price_at_time": "10.00"
    }

    serializer = CartItemSerializer(data=data)

    assert serializer.is_valid() is True
    
    with pytest.raises(serializers.ValidationError, match= "stock"):
        serializer.save()