import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_register_view(client):
    url = reverse("customers:register")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "strongpassword"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data["username"] == "newuser"
    assert response.data["email"] == "newuser@example.com"
    assert "password" not in response.data

    assert User.objects.filter(username="newuser").exists()

    user = User.objects.get(username="newuser")
    assert user.check_password("strongpassword")
    assert hasattr(user, 'profile')


@pytest.mark.django_db
def test_register_view_invalid_email(client):
    User.objects.create_user(username="existinguser", email="existing@example.com")
    url = reverse("customers:register")
    data = {
        "username": "newuser",
        "email": "existing@example.com",
        "password": "strongpassword"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert "email" in response.data

@pytest.mark.django_db
def test_register_view_invalid_username(client):
    User.objects.create_user(username="existinguser")
    url = reverse("customers:register")
    data = {
        "username": "existinguser",
        "email": "newuser@example.com",
        "password": "strongpassword"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert "username" in response.data

@pytest.mark.django_db
def test_register_view_invalid_password(client):
    url = reverse("customers:register")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "weak"
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert "password" in response.data
    
@pytest.mark.django_db
def test_register_view_missing_fields(client):
    url = reverse("customers:register")

    response = client.post(url, {}, format='json')
    assert response.status_code == 400
    assert "username" in response.data
    assert "email" in response.data
    assert "password" in response.data