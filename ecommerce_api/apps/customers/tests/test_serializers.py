import pytest
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile
from apps.customers.serializer import CustomerProfileSerializer

@pytest.mark.django_db
def test_customerprofile_serializer_data():
    user = User.objects.create_user(username="matheus", email="m@x.com", password="123")
    profile = CustomerProfile.objects.create(
        user=user,
        phone="123",
        address="Rua Y",
        city="BH",
        state="MG"
    )

    serializer = CustomerProfileSerializer(profile)
    data = serializer.data

    assert data["username"] == "matheus"
    assert data["email"] == "m@x.com"
    assert data["phone"] == "123"
    assert "created_at" in data
    assert "user" in data


@pytest.mark.django_db
def test_customerprofile_serializer_create():
    user = User.objects.create_user(username="novo")

    data = {
        "user": user.id,
        "phone": "999",
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is True

    instance = serializer.save()
    assert instance.phone == "999"

@pytest.mark.django_db
def test_invalid_customerprofile_serializer():
    data = {
        "user": None,
        "phone": "",
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "user" in serializer.errors
    assert "phone" in serializer.errors