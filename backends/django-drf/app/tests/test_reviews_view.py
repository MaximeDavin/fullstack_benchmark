import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

PAGE_SIZE = 10


@pytest.fixture
def api_client():
    return APIClient()


def test_list_reviews(api_client, movie_data):
    url = reverse("review-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == PAGE_SIZE
    assert response.data["count"] == 12


def test_filter_reviews_by_movie(api_client, movie_data):
    movies, _, _ = movie_data
    url = reverse("review-list")
    response = api_client.get(url, {"movie": movies[0].id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 6
    assert response.data["count"] == 6


def test_filter_reviews_by_user(api_client, movie_data):
    _, _, users = movie_data
    url = reverse("review-list")
    response = api_client.get(url, {"user": users[0].id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2
    assert response.data["count"] == 2


def test_order_reviews_by_created_at(api_client, movie_data):
    url = reverse("review-list")
    response = api_client.get(url, {"ordering": "created_at"})

    assert response.status_code == status.HTTP_200_OK
    # Verify the reviews are ordered by created_at
    created_at_order = [review["created_at"] for review in response.data["results"]]
    assert created_at_order == sorted(created_at_order)


def test_order_reviews_by_rating(api_client, movie_data):
    _, _, users = movie_data
    url = reverse("review-list")
    response = api_client.get(url, {"ordering": "rating"})

    assert response.status_code == status.HTTP_200_OK
    # Verify the reviews are ordered by created_at
    created_at_order = [review["rating"] for review in response.data["results"]]
    assert created_at_order == sorted(created_at_order)


def test_create_review(api_client, movie_data):
    movies, _, users = movie_data
    api_client.force_authenticate(user=users[0])

    url = reverse("review-list")
    payload = {"movie": movies[2].id, "rating": 5, "review": "A masterpiece!"}
    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["movie"] == movies[2].id
    assert response.data["rating"] == 5
    assert response.data["review"] == "A masterpiece!"


def test_update_review_authorized(api_client, movie_data):
    _, reviews, users = movie_data
    api_client.force_authenticate(user=users[0])

    url = reverse("review-detail", args=[reviews[0].id])
    payload = {
        "review": "test review",
    }
    response = api_client.patch(url, payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["review"] == "test review"


def test_update_review_unauthorized(api_client, movie_data):
    _, reviews, users = movie_data
    api_client.force_authenticate(user=users[0])

    url = reverse("review-detail", args=[reviews[1].id])
    payload = {
        "review": "test review",
    }
    response = api_client.patch(url, payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_review_authorized(api_client, movie_data):
    _, reviews, users = movie_data
    api_client.force_authenticate(user=users[0])

    url = reverse("review-detail", args=[reviews[0].id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_review_unauthorized(api_client, movie_data):
    _, reviews, users = movie_data
    api_client.force_authenticate(user=users[0])

    url = reverse("review-detail", args=[reviews[1].id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_retrieve_review(api_client, movie_data):
    _, reviews, users = movie_data
    url = reverse("review-detail", args=[reviews[1].id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == reviews[1].id
    assert response.data["rating"] == reviews[1].rating
    assert response.data["review"] == reviews[1].review
    assert response.data["user"] == users[1].username
