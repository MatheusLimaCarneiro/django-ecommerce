import pytest
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile

@pytest.mark.django_db
def test_create_customer_profile():
    user = User.objects.create_user(username="matheus", password="123")

    profile = CustomerProfile.objects.create(
        user=user,
        phone="123456789",
        address="Rua Teste",
        city="São Paulo",
        state="SP"
    )

    assert profile.user.username == "matheus"
    assert profile.phone == "123456789"
    assert profile.address == "Rua Teste"
    assert profile.city == "São Paulo"
    assert profile.state == "SP"

@pytest.mark.django_db
def test_customerprofile_str():
    user = User.objects.create_user(username="maria", password="123")
    profile = CustomerProfile.objects.create(
        user=user,
        phone="999999",
        address="Rua X",
        city="Rio",
        state="RJ"
    )
    assert str(profile) == "maria"


@pytest.mark.django_db
def test_customerprofile_ordering():
    user1 = User.objects.create_user(username="u1")
    user2 = User.objects.create_user(username="u2")

    p1 = CustomerProfile.objects.create(user=user1, phone="1", address="a", city="a", state="a")
    p2 = CustomerProfile.objects.create(user=user2, phone="2", address="b", city="b", state="b")

    profiles = CustomerProfile.objects.all()
    assert list(profiles) == [p1, p2] 