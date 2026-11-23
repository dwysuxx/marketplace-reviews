import pytest

from reviews import ReviewBook, ReviewError


@pytest.fixture
def book():
    b = ReviewBook()
    b.register_purchase("anna", "phone")
    b.register_purchase("ivan", "phone")
    b.register_purchase("olha", "phone")
    return b


def test_add_review_and_average(book):
    book.add_review("anna", "phone", 5, "Чудовий телефон")
    book.add_review("ivan", "phone", 4)
    assert book.average_rating("phone") == 4.5


def test_average_rounded_to_one_decimal(book):
    for user, rating in [("anna", 5), ("ivan", 4), ("olha", 4)]:
        book.add_review(user, "phone", rating)
    assert book.average_rating("phone") == 4.3  # 13 / 3 = 4.333...


def test_no_reviews_gives_none(book):
    assert book.average_rating("phone") is None


@pytest.mark.parametrize("rating", [1, 5])
def test_boundary_ratings_accepted(book, rating):
    book.add_review("anna", "phone", rating)
    assert book.average_rating("phone") == rating


@pytest.mark.parametrize("rating", [0, 6, -1, 4.5, "5", True, None])
def test_invalid_rating_rejected(book, rating):
    with pytest.raises(ReviewError):
        book.add_review("anna", "phone", rating)


def test_only_buyer_can_review(book):
    with pytest.raises(ReviewError):
        book.add_review("petro", "phone", 5)


def test_one_review_per_buyer(book):
    book.add_review("anna", "phone", 5)
    with pytest.raises(ReviewError):
        book.add_review("anna", "phone", 1)


def test_text_length_limit(book):
    book.add_review("anna", "phone", 4, "a" * 1000)
    with pytest.raises(ReviewError):
        book.add_review("ivan", "phone", 4, "a" * 1001)
