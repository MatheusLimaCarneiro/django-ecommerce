import pytest
from apps.reviews.serializer import ReviewSerializer
from apps.reviews.tests.factories import ReviewFactory, ProductFactory, CustomerProfileFactory, OrderFactory, OrderItemFactory
from django.utils import timezone

@pytest.mark.django_db
def test_review_serializer():
    review = ReviewFactory()
    serializer = ReviewSerializer(instance=review)
    data = serializer.data

    assert data["id"] == review.id
    assert data["product"] == review.product.id
    assert data["customer"] == review.customer.id
    assert data["rating"] == review.rating
    assert data["comment"] == review.comment
    assert data["created_at"] == timezone.localtime(review.created_at).isoformat()

@pytest.mark.django_db
def test_review_serializer_create():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    data = {
        "rating": 4,
        "comment": "Good product"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is True
    assert serializer.errors == {}
    instance = serializer.save()
    
    assert instance.product == product
    assert instance.customer == customer
    assert instance.rating == 4
    assert instance.comment == "Good product"
    assert instance.id is not None

@pytest.mark.django_db
def test_review_serializer_invalid_duplicate_review():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    ReviewFactory(
        product=product,
        customer=customer
    )

    data = {
        "rating": 5,
        "comment": "Excellent!"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_invalid_not_purchased():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    data = {
        "rating": 3,
        "comment": "Average product"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_invalid_rating_above_max():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    data = {
        "rating": 10,
        "comment": "Too good to be true"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is False
    assert "rating" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_invalid_rating_below_min():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    data = {
        "rating": 0,
        "comment": "Bad product"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is False
    assert "rating" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_missing_context():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    data = {
        "rating": 4,
        "comment": "Good product"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product}  # Missing customer
    )
    
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

    serializer = ReviewSerializer(
        data=data,
        context={"customer": customer}  # Missing product
    )
    
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_invalid_missing_rating():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    data = {
        "comment": "No rating provided"
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is False
    assert "rating" in serializer.errors

@pytest.mark.django_db
def test_review_serializer_create_without_comment():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    order = OrderFactory(customer=customer, payment_status='PAID')
    
    OrderItemFactory(order=order, product=product)

    data = {
        "rating": 5
    }

    serializer = ReviewSerializer(
        data=data,
        context={"product": product, "customer": customer}
    )
    
    assert serializer.is_valid() is True
    assert serializer.errors == {}
    instance = serializer.save()
    
    assert instance.product == product
    assert instance.customer == customer
    assert instance.rating == 5
    assert instance.comment == ""  # Default empty comment
    assert instance.id is not None

@pytest.mark.django_db
def test_review_serializer_invalid_no_context():
    data = {
        "rating": 4,
        "comment": "Good product"
    }

    serializer = ReviewSerializer(
        data=data,
        context={}  # No product or customer in context
    )
    
    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors