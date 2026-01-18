import factory
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile
from apps.categories.models import Category
from apps.products.models import Product
from apps.orders.models import Order
from apps.order_items.models import OrderItem


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "123")

class CustomerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerProfile

    user = factory.SubFactory(UserFactory)

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = "Sample product description"
    price = 10.00
    category = factory.SubFactory(CategoryFactory)
    stock = 100
    is_active = True

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerProfileFactory)
    status = "PENDING"
    payment_status = "UNPAID"
    total_amount = 0.00

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
    subtotal = factory.LazyAttribute(lambda o: o.unit_price * o.quantity)