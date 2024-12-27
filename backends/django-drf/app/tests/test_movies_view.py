import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_list_movies(api_client, movie_data):
    response = api_client.get(reverse("movie-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3

    titles = [movie["title"] for movie in response.data["results"]]
    assert "Inception" in titles
    assert "The Matrix" in titles
    assert "The Godfather" in titles


def test_filter_movies_by_year(api_client, movie_data):
    response = api_client.get(reverse("movie-list"), {"year": 2010})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "Inception"


def test_order_movies_by_release_date_asc(api_client, movie_data):
    response = api_client.get(reverse("movie-list"), {"ordering": "released_at"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == "the-godfather"
    assert response.data["results"][1]["id"] == "the-matrix"
    assert response.data["results"][2]["id"] == "inception"


def test_order_movies_by_release_date_desc(api_client, movie_data):
    response = api_client.get(reverse("movie-list"), {"ordering": "-released_at"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == "inception"
    assert response.data["results"][1]["id"] == "the-matrix"
    assert response.data["results"][2]["id"] == "the-godfather"


def test_order_movies_by_title(api_client, movie_data):
    response = api_client.get(reverse("movie-list"), {"ordering": "title"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == "inception"
    assert response.data["results"][1]["id"] == "the-godfather"
    assert response.data["results"][2]["id"] == "the-matrix"


def test_get_movie(api_client, movie_data, django_assert_num_queries):
    movies, reviews, users = movie_data
    with django_assert_num_queries(3):
        response = api_client.get(reverse("movie-detail", args=(movies[0].id,)))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == movies[0].id
    assert len(response.data["reviews"]) == 5
    assert response.data["reviews"][0]["user"] == users[-1].username
