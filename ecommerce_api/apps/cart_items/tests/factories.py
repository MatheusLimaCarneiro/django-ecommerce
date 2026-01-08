import factory
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile
from apps.carts.models import Cart
from apps.categories.models import Category
from apps.products.models import Product
from apps.cart_items.models import CartItem


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


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(CustomerProfileFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = "Test category"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    category = factory.SubFactory(CategoryFactory)
    price = 10.00
    stock = 100
    description = "Test product"
    is_active = True


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 2
    price_at_time = 10.00