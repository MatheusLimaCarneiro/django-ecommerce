import factory
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile
from apps.orders.models import Order

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

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerProfileFactory)
    status = "PENDING"
    payment_status = "UNPAID"
    total_amount = 0.00