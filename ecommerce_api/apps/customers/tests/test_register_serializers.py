import pytest
from django.contrib.auth.models import User
from apps.customers.registerSerializer import RegisterSerializer

@pytest.mark.django_db
def test_register_serializer_valid_data():
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "strongpassword"
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is True
    user = serializer.save()
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.check_password("strongpassword") is True
    assert hasattr(user, 'profile') is True

@pytest.mark.django_db
def test_register_serializer_invalid_email():
    User.objects.create_user(username="existinguser", email="existing@example.com")

    data = {
        "username": "newuser",
        "email": "existing@example.com",
        "password": "strongpassword"
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_invalid_username():
    User.objects.create_user(username="existinguser")

    data = {
        "username": "existinguser",
        "email": "existing@example.com",
        "password": "strongpassword"
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert "username" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_invalid_password():
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "short"
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert "password" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_missing_fields():
    data = {
        "username": "newuser"
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert "email" in serializer.errors
    assert "password" in serializer.errors