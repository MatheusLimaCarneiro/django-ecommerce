import pytest
from apps.orders.models import Order
from django.core.exceptions import ValidationError
from apps.orders.tests.factories import OrderFactory, CustomerProfileFactory, UserFactory

@pytest.mark.django_db
def test_create_order():
    order = OrderFactory()
    assert order.id is not None
    assert order.status == "PENDING"
    assert order.payment_status == "UNPAID"
    assert order.total_amount == 0.00

@pytest.mark.django_db
def test_order_str():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile)
    expected_str = f"Order {order.id} for {customer_profile}"
    assert str(order) == expected_str

@pytest.mark.django_db
def test_order_ordering():
    order1 = OrderFactory()
    order2 = OrderFactory()

    orders = Order.objects.all()
    assert list(orders.order_by('id')) == [order1, order2]

@pytest.mark.django_db
def test_order_total_amount_min_value():
    order = OrderFactory(total_amount=-10.00)
    with pytest.raises(ValidationError) as exc:
        order.full_clean()
    
    assert "total_amount" in str(exc.value)

@pytest.mark.django_db
def test_order_factory():
    user = UserFactory()
    customer_profile = CustomerProfileFactory(user=user)
    order = OrderFactory(customer=customer_profile)

    assert isinstance(order.customer, type(customer_profile))
    assert order.status == "PENDING"
    assert order.payment_status == "UNPAID"
    assert order.total_amount == 0.00

@pytest.mark.django_db
def test_order_customer_relationship():
    customer_profile = CustomerProfileFactory()
    order = OrderFactory(customer=customer_profile)

    assert order.customer == customer_profile
    assert order in customer_profile.orders.all()