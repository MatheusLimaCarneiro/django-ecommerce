import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.customers.models import CustomerProfile

@pytest.mark.django_db
def test_customerprofile_list_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    CustomerProfile.objects.create(
        user=user, phone="1", address="a", city="a", state="a"
    )

    url = reverse("customers:customers-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_customerprofile_retrieve_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    profile = CustomerProfile.objects.create(
        user=user, phone="1", address="a", city="a", state="a"
    )

    url = reverse("customers:customers-detail", args=[profile.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == "u1"


@pytest.mark.django_db
def test_customerprofile_create_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    url = reverse("customers:customers-list")
    data = {
        "phone": "333",
        "address": "Rua XPTO",
        "city": "SP",
        "state": "SP",
    }

    response = client.post(url, data)
    assert response.status_code == 201
    assert CustomerProfile.objects.count() == 1


@pytest.mark.django_db
def test_customerprofile_update_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)

    profile = CustomerProfile.objects.create(
        user=user, phone="111", address="A", city="A", state="A"
    )

    url = reverse("customers:customers-detail", args=[profile.id])
    data = {
        "phone": "999",
        "address": "Nova Rua",
        "city": "RJ",
        "state": "RJ",
    }

    response = client.put(url, data)
    assert response.status_code == 200
    profile.refresh_from_db()
    assert profile.phone == "999"


@pytest.mark.django_db
def test_customerprofile_delete_view():
    client = APIClient()

    user = User.objects.create_user(username="u1")
    client.force_authenticate(user=user)
    profile = CustomerProfile.objects.create(
        user=user, phone="111", address="A", city="A", state="A"
    )

    url = reverse("customers:customers-detail", args=[profile.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert CustomerProfile.objects.count() == 0
