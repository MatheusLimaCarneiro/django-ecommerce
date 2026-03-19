import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile

@pytest.mark.django_db
def test_customerprofile_me_retrieve_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    profile = CustomerProfile.objects.create(
        user=user, phone="1", address="a", city="a", state="a"
    )

    url = reverse("customers:customers-me")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == "u1"
    assert response.data["email"] == ""
    assert response.data["phone"] == "1"
    assert response.data["address"] == "a"
    assert response.data["city"] == "a"
    assert response.data["state"] == "a"

@pytest.mark.django_db
def test_customerprofile_me_update_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    profile = CustomerProfile.objects.create(
        user=user, phone="111", address="A", city="A", state="A"
    )

    url = reverse("customers:customers-me")
    data = {
        "phone": "999",
        "address": "Nova Rua",
        "city": "RJ",
        "state": "RJ",
    }

    response = client.patch(url, data)
    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.phone == "999"
    assert profile.address == "Nova Rua"
    assert profile.city == "RJ"
    assert profile.state == "RJ"