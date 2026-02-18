import pytest
from apps.order_items.models import OrderItem
from django.core.exceptions import ValidationError
from apps.order_items.tests.factories import OrderItemFactory, OrderFactory, ProductFactory, CustomerProfileFactory, UserFactory
from apps.orders.models import Order
from apps.products.models import Product

@pytest.mark.django_db
def test_create_order_item():
    order_item = OrderItemFactory()
    assert order_item.id is not None
    assert order_item.quantity == 1
    assert order_item.unit_price == order_item.product.price
    assert order_item.subtotal == order_item.unit_price * order_item.quantity

@pytest.mark.django_db
def test_order_item_str():
    order_item = OrderItemFactory()
    expected_str = f'OrderItem #{order_item.id} | Order #{order_item.order_id} | Product #{order_item.product_id}'
    assert str(order_item) == expected_str

@pytest.mark.django_db
def test_unique_product_per_order_constraint():
    order = OrderFactory()
    product = ProductFactory()

    OrderItemFactory(order=order, product=product)

    with pytest.raises(ValidationError) as excinfo:
        duplicate_item = OrderItem(
            order=order,
            product=product,
            quantity=2,
            unit_price=product.price,
            subtotal=product.price * 2
        )
        duplicate_item.full_clean()

    assert '__all__' in excinfo.value.message_dict


@pytest.mark.django_db
def test_order_item_quantity_min_value():
    order = OrderFactory()
    product = ProductFactory()

    with pytest.raises(ValidationError) as excinfo:
        invalid_item = OrderItem(
            order=order,
            product=product,
            quantity=0,
            unit_price=product.price,
            subtotal=0
        )
        invalid_item.full_clean()

    assert 'quantity' in str(excinfo.value.message_dict)

@pytest.mark.django_db
def test_order_item_unit_price_min_value():
    order = OrderFactory()
    product = ProductFactory()

    with pytest.raises(ValidationError) as excinfo:
        invalid_item = OrderItem(
            order=order,
            product=product,
            quantity=1,
            unit_price=-10,
            subtotal=-10
        )
        invalid_item.full_clean()

    assert 'unit_price' in str(excinfo.value.message_dict)

@pytest.mark.django_db
def test_order_item_subtotal_min_value():
    order = OrderFactory()
    product = ProductFactory()

    with pytest.raises(ValidationError) as excinfo:
        invalid_item = OrderItem(
            order=order,
            product=product,
            quantity=1,
            unit_price=product.price,
            subtotal=-5
        )
        invalid_item.full_clean()

    assert 'subtotal' in str(excinfo.value.message_dict)

@pytest.mark.django_db
def test_order_item_ordering():
    order_item1 = OrderItemFactory()
    order_item2 = OrderItemFactory()
    order_item3 = OrderItemFactory()

    order_items = OrderItem.objects.all()
    assert list(order_items.order_by('id')) == [order_item1, order_item2, order_item3]

@pytest.mark.django_db
def test_order_item_factory():
    order_item = OrderItemFactory()
    assert isinstance(order_item.order, Order)
    assert isinstance(order_item.product, Product)
    assert order_item.quantity == 1
    assert order_item.unit_price == order_item.product.price
    assert order_item.subtotal == order_item.unit_price * order_item.quantity

@pytest.mark.django_db
def test_order_item_negative_unit_price_validation():
    order = OrderFactory()
    product = ProductFactory()

    with pytest.raises(ValidationError) as excinfo:
        invalid_item = OrderItem(
            order=order,
            product=product,
            quantity=1,
            unit_price=-1,
            subtotal=-1
        )
        invalid_item.full_clean()

    assert 'unit_price' in str(excinfo.value.message_dict)