import factory
from apps.reviews.models import Review
from apps.orders.models import Order
from apps.order_items.models import OrderItem
from apps.categories.models import Category
from apps.products.models import Product
from apps.customers.models import CustomerProfile
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

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
    description = "A sample category."

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    category = factory.SubFactory(CategoryFactory)
    description = "A sample product"
    price = Decimal("10.00")
    stock = 100
    is_active = True

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerProfileFactory)
    rating = 5
    comment = "Great product!"
    created_at = factory.LazyFunction(timezone.now)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerProfileFactory)
    total_amount = Decimal("50.00")
    status = "PENDING"
    created_at = factory.LazyFunction(timezone.now)

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 2
    unit_price = Decimal("25.00")
    subtotal = factory.LazyAttribute(lambda o: o.quantity * o.unit_price)