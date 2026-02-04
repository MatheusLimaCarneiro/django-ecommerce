import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from apps.reviews.tests.factories import ReviewFactory, ProductFactory, CustomerProfileFactory, OrderFactory, OrderItemFactory

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_review_list_view(client):
    review = ReviewFactory()
    customer = review.customer.user

    client.force_authenticate(user=customer)

    url = reverse("reviews:reviews-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    assert response.data[0]["id"] == review.id
    assert response.data[0]["product"] == review.product.id
    assert response.data[0]["customer"] == review.customer.id
    assert response.data[0]["rating"] == review.rating
    assert response.data[0]["comment"] == review.comment
    assert response.data[0]["created_at"] == timezone.localtime(review.created_at).isoformat()

@pytest.mark.django_db
def test_review_retrieve_view(client):
    review = ReviewFactory()
    customer = review.customer.user

    client.force_authenticate(user=customer)

    url = reverse("reviews:reviews-detail", args=[review.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == review.id
    assert response.data["product"] == review.product.id
    assert response.data["customer"] == review.customer.id
    assert response.data["rating"] == review.rating
    assert response.data["comment"] == review.comment
    assert response.data["created_at"] == timezone.localtime(review.created_at).isoformat()

@pytest.mark.django_db
def test_review_create_view(client):
    product = ProductFactory()
    customer_profile = CustomerProfileFactory()

    order = OrderFactory(customer=customer_profile, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "rating": 5,
        "comment": "Excellent product"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data["id"] is not None
    assert response.data["product"] == product.id
    assert response.data["customer"] == customer_profile.id
    assert response.data["rating"] == 5
    assert response.data["comment"] == "Excellent product"
    assert response.data["created_at"] is not None

@pytest.mark.django_db
def test_review_create_view_unauthenticated(client):
    product = ProductFactory()

    data = {
        "rating": 5,
        "comment": "Excellent product"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_review_create_view_no_purchase(client):
    product = ProductFactory()
    customer_profile = CustomerProfileFactory()
    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "rating": 3,
        "comment": "Average product"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_review_create_view_duplicate_review(client):
    product = ProductFactory()
    customer_profile = CustomerProfileFactory()

    order = OrderFactory(customer=customer_profile, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    ReviewFactory(
        product=product,
        customer=customer_profile
    )

    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "rating": 4,
        "comment": "Good product"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    
@pytest.mark.django_db
def test_review_create_view_rating_above_range(client):
    product = ProductFactory()
    customer_profile = CustomerProfileFactory()

    order = OrderFactory(customer=customer_profile, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "rating": 6,
        "comment": "Invalid rating"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "rating" in response.data

@pytest.mark.django_db
def test_review_create_view_rating_below_range(client):
    product = ProductFactory()
    customer_profile = CustomerProfileFactory()

    order = OrderFactory(customer=customer_profile, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    customer = customer_profile.user

    client.force_authenticate(user=customer)

    data = {
        "rating": 0,
        "comment": "Invalid rating"
    }
    url = reverse("products:products-reviews", args=[product.id])
    response = client.post(url, data, format='json')

    assert response.status_code == 400
    assert "rating" in response.data