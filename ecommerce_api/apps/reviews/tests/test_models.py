import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.reviews.models import Review
from apps.reviews.tests.factories import ReviewFactory, ProductFactory, CustomerProfileFactory

@pytest.mark.django_db
def test_create_review():
    review = ReviewFactory()
    assert review.id is not None
    assert 1 <= review.rating <= 5
    assert review.comment == "Great product!"
    assert review.product is not None
    assert review.customer is not None

@pytest.mark.django_db
def test_review_str():
    review = ReviewFactory()
    expected_str = f"Review #{review.id} | Product #{review.product} | Customer #{review.customer} | Rating: {review.rating}"
    assert str(review) == expected_str

@pytest.mark.django_db
def test_unique_review_constraint():
    product = ProductFactory()
    customer = CustomerProfileFactory()

    ReviewFactory(product=product, customer=customer)

    with pytest.raises(IntegrityError):
        Review.objects.create(
            product=product,
            customer=customer,
            rating=4,
            comment="Another review"
        )

@pytest.mark.django_db
def test_rating_value_constraints():
    product = ProductFactory()
    customer = CustomerProfileFactory()
    
    with pytest.raises(ValidationError) as excinfo_low:
        review = Review(
            product=product,
            customer=customer,
            rating=0,
            comment="Invalid low rating"
        )
        review.full_clean()

    assert 'rating' in excinfo_low.value.message_dict
    assert excinfo_low.value.message_dict['rating']
    
    with pytest.raises(ValidationError) as excinfo_high:
        review = Review(
            product=product,
            customer=customer,
            rating=6,
            comment="Invalid high rating"
        )
        review.full_clean()

    assert 'rating' in excinfo_high.value.message_dict
    assert excinfo_high.value.message_dict['rating']

@pytest.mark.django_db
def test_review_ordering():
    product = ProductFactory()
    customer = CustomerProfileFactory()
    customer2 = CustomerProfileFactory()
    
    review1 = ReviewFactory(product=product, customer=customer, rating=4)
    review2 = ReviewFactory(product=product, customer=customer2, rating=5)

    reviews = list(Review.objects.filter(product=product).order_by('-created_at', 'id'))
    
    assert reviews[0] == review2
    assert reviews[1] == review1