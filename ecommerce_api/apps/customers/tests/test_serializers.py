import pytest
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile
from apps.customers.serializers.customer import CustomerProfileSerializer

@pytest.mark.django_db
def test_customerprofile_serializer_data():
    user = User.objects.create_user(username="matheus", email="m@x.com", password="123")
    profile = CustomerProfile.objects.create(
        user=user,
        phone="12345",
        address="Rua Y",
        city="BH",
        state="MG"
    )

    serializer = CustomerProfileSerializer(profile)
    data = serializer.data

    assert data["username"] == "matheus"
    assert data["email"] == "m@x.com"
    assert data["phone"] == "12345"
    assert data["address"] == "Rua Y"
    assert data["city"] == "BH"
    assert "created_at" in data


@pytest.mark.django_db
def test_customerprofile_serializer_create():
    user = User.objects.create_user(username="novo")

    data = {
        "phone": "99999",
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid()

    instance = serializer.save(user=user)
    assert instance.phone == "99999"
    assert instance.address == "Rua Teste"
    assert instance.city == "SP"
    assert instance.state == "SP"

@pytest.mark.django_db
def test_customerprofile_serializer_phone_invalid():
    data = {
        "phone": "abcde",
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "phone" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_phone_too_short():
    data = {
        "phone": "123",
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "phone" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_phone_too_long():
    data = {
        "phone": "1" * 21,
        "address": "Rua Teste",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "phone" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_address_too_short():
    data = {
        "phone": "12345",
        "address": "Rua",
        "city": "SP",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "address" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_city_invalid():
    data = {
        "phone": "12345",
        "address": "Rua Teste",
        "city": "SP1",
        "state": "SP"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "city" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_state_invalid():
    data = {
        "phone": "12345",
        "address": "Rua Teste",
        "city": "SP",
        "state": "S1"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is False
    assert "state" in serializer.errors

@pytest.mark.django_db
def test_customerprofile_state_uppercase():
    data = {
        "phone": "12345",
        "address": "Rua Teste",
        "city": "SP",
        "state": "sp"
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid() is True

    instance = serializer.save(user=User.objects.create_user(username="test"))
    assert instance.state == "SP"

@pytest.mark.django_db
def test_customerprofile_strip_fields():
    data = {
        "phone": " 12345 ",
        "address": " Rua Teste ",
        "city": " SP ",
        "state": " SP "
    }

    serializer = CustomerProfileSerializer(data=data)
    assert serializer.is_valid()

    instance = serializer.save(user=User.objects.create_user(username="test2"))
    assert instance.phone == "12345"
    assert instance.address == "Rua Teste"
    assert instance.city == "SP"
    assert instance.state == "SP"