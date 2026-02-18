import pytest
from apps.orders.models import Order
from django.core.exceptions import ValidationError
from apps.orders.tests.factories import OrderFactory, CustomerProfileFactory, UserFactory, OrderItemFactory
from decimal import Decimal

@pytest.mark.django_db
def test_create_order():
    order = OrderFactory()
    assert order.id is not None
    assert order.status == Order.Status.PENDING
    assert order.payment_status == Order.PaymentStatus.UNPAID
    assert order.total_amount == Decimal("0.00")

@pytest.mark.django_db
def test_order_str():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile)
    expected_str = f"Order #{order.id} | Customer #{customer_profile.id}"
    assert str(order) == expected_str

@pytest.mark.django_db
def test_order_ordering():
    order1 = OrderFactory()
    order2 = OrderFactory()

    orders = Order.objects.all()
    assert list(orders.order_by('id')) == [order1, order2]

@pytest.mark.django_db
def test_order_factory():
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)

    assert isinstance(order.customer, type(customer_profile))
    assert order.status == Order.Status.PENDING
    assert order.payment_status == Order.PaymentStatus.UNPAID
    assert order.total_amount == 0.00

@pytest.mark.django_db
def test_order_customer_relationship():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile)

    assert order.customer == customer_profile
    assert order in customer_profile.orders.all()

@pytest.mark.django_db
def test_update_total_amount():
    order = OrderFactory()

    OrderItemFactory(order=order, quantity=2, unit_price=Decimal('15.00'), subtotal=Decimal('30.00'))
    OrderItemFactory(order=order, quantity=1, unit_price=Decimal('20.00'), subtotal=Decimal('20.00'))

    order.update_total_amount()

    order.refresh_from_db()
    assert order.total_amount == Decimal('50.00')

@pytest.mark.django_db
def test_update_total_amount_with_no_items_sets_zero():
    order = OrderFactory()

    order.update_total_amount()
    order.refresh_from_db()

    assert order.total_amount == Decimal('0.00')


@pytest.mark.django_db
def test_order_status_choices():
    order = OrderFactory(status=Order.Status.CONFIRMED)
    assert order.status == order.Status.CONFIRMED

    with pytest.raises(ValidationError):
        order.status = 'INVALID_STATUS'
        order.full_clean()

@pytest.mark.django_db
def test_order_payment_status_choices():
    order = OrderFactory(payment_status=Order.PaymentStatus.PAID)
    assert order.payment_status == order.PaymentStatus.PAID

    with pytest.raises(ValidationError):
        order.payment_status = 'INVALID_STATUS'
        order.full_clean()

@pytest.mark.django_db
def test_mark_order_as_paid():
    order = OrderFactory()
    order.mark_as_paid()

    order.refresh_from_db()
    assert order.payment_status == Order.PaymentStatus.PAID