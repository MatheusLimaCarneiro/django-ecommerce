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