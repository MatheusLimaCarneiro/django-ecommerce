import pytest
from apps.cart_items.models import CartItem
from apps.carts.models import Cart
from apps.products.models import Product
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.cart_items.tests.factories import CartItemFactory

@pytest.mark.django_db
def test_create_cart_item():
    cart_item = CartItemFactory()
    assert cart_item.id is not None
    assert cart_item.quantity == 2
    assert cart_item.price_at_time == 10.00

@pytest.mark.django_db
def test_cart_item_str():
    cart_item = CartItemFactory(quantity=3)
    expected_str = f"CartItem #{cart_item.id} | Cart #{cart_item.cart_id} | Product #{cart_item.product_id}"
    assert str(cart_item) == expected_str

@pytest.mark.django_db
def test_cart_item_unique_together():
    cart_item1 = CartItemFactory()
    with pytest.raises(IntegrityError):
        CartItemFactory(cart=cart_item1.cart, product=cart_item1.product)
    
@pytest.mark.django_db
def test_cart_item_ordering():
    cart_item1 = CartItemFactory()
    cart_item2 = CartItemFactory()

    items = CartItem.objects.all()
    assert list(items.order_by('id')) == [cart_item1, cart_item2]

@pytest.mark.django_db
def test_cart_item_quantity_min_value():
    cart_item = CartItemFactory( quantity=0 )
    with pytest.raises(ValidationError) as exc:
        cart_item.full_clean()
    
    assert "quantity" in str(exc.value)

@pytest.mark.django_db
def test_cart_item_price_at_time_min_value():
    cart_item = CartItemFactory( price_at_time=-5.00 )
    with pytest.raises(ValidationError) as exc:
        cart_item.full_clean()
    
    assert "price_at_time" in str(exc.value)

@pytest.mark.django_db
def test_cart_item_factory():
    cart_item = CartItemFactory()
    assert isinstance(cart_item.cart, Cart)
    assert isinstance(cart_item.product, Product)
    assert cart_item.quantity == 2
    assert cart_item.price_at_time == 10.00