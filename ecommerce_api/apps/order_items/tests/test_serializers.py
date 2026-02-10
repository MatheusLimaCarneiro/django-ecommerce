import pytest
from decimal import Decimal
from apps.order_items.serializer import OrderItemSerializer
from apps.order_items.tests.factories import OrderItemFactory, OrderFactory, ProductFactory

@pytest.mark.django_db
def test_order_item_serializer():
    order_item = OrderItemFactory()
    serializer = OrderItemSerializer(instance=order_item)
    data = serializer.data

    assert data["id"] == order_item.id
    assert data["product"] == order_item.product.id
    assert data["quantity"] == order_item.quantity
    assert str(data["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(data["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_serializer_create():
    order = OrderFactory()
    product = ProductFactory(stock=10, price=Decimal("15.00"))

    data = {
        "product": product.id,
        "quantity": 2
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.order == order
    assert instance.product == product
    assert instance.quantity == 2
    assert instance.unit_price == Decimal("15.00")
    assert instance.subtotal == Decimal("30.00")
    assert instance.id is not None

@pytest.mark.django_db
def test_order_item_serializer_invalid_product_inactive():
    order = OrderFactory()
    product = ProductFactory(is_active=False)

    data = {
        "product": product.id,
        "quantity": 1
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_order_item_serializer_invalid_product_out_of_stock():
    order = OrderFactory()
    product = ProductFactory(stock=0)

    data = {
        "product": product.id,
        "quantity": 1
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_order_item_serializer_invalid_insufficient_stock():
    order = OrderFactory()
    product = ProductFactory(stock=5)

    data = {
        "product": product.id,
        "quantity": 10
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_order_item_serializer_read_only_fields():
    order_item = OrderItemFactory()
    serializer = OrderItemSerializer(instance=order_item)
    data = serializer.data

    assert str(data["unit_price"]) == f"{order_item.unit_price:.2f}"
    assert str(data["subtotal"]) == f"{order_item.subtotal:.2f}"

@pytest.mark.django_db
def test_order_item_serializer_create_with_zero_quantity():
    order = OrderFactory()
    product = ProductFactory(stock=10)

    data = {
        "product": product.id,
        "quantity": 0
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "quantity" in serializer.errors

@pytest.mark.django_db
def test_order_item_serializer_create_with_negative_quantity():
    order = OrderFactory()
    product = ProductFactory(stock=10)

    data = {
        "product": product.id,
        "quantity": -5
    }
    serializer = OrderItemSerializer(data=data, context={"order": order})
    assert serializer.is_valid() is False
    assert "quantity" in serializer.errors