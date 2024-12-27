from ..serializers import (
    DetailMovieSerializer,
    ListMovieSerializer,
    ReadReviewSerializer,
)


def test_list_movie_serializer(movie_data):
    movies, _, _ = movie_data
    serializer = ListMovieSerializer([movies[0], movies[1]], many=True)
    assert len(serializer.data) == 2

    movie_data = serializer.data[0]
    assert movie_data["id"] == movies[0].id
    assert movie_data["title"] == movies[0].title
    assert movie_data["year"] == movies[0].year
    assert movie_data["description"] == movies[0].description
    assert movie_data["released_at"] == movies[0].released_at

    movie_data = serializer.data[1]
    assert movie_data["id"] == movies[1].id
    assert movie_data["title"] == movies[1].title
    assert movie_data["year"] == movies[1].year
    assert movie_data["description"] == movies[1].description
    assert movie_data["released_at"] == movies[1].released_at


def test_detail_movie_serializer(movie_data):
    movies, _, users = movie_data

    serializer = DetailMovieSerializer(instance=movies[0])
    movie_data = serializer.data

    assert movie_data["id"] == movies[0].id
    assert movie_data["title"] == movies[0].title
    assert movie_data["year"] == movies[0].year
    assert movie_data["description"] == movies[0].description
    assert movie_data["released_at"] == movies[0].released_at
    assert len(movie_data["reviews"]) == 5

    assert movie_data["reviews"][0]["user"] == users[-1].username

    # Verify the reviews are ordered by created_at
    created_at_order = [
        review_data["created_at"] for review_data in movie_data["reviews"]
    ]
    assert created_at_order == list(reversed(sorted(created_at_order)))


def test_read_review_serializer(movie_data):
    _, reviews, users = movie_data
    review = reviews[0]
    serializer = ReadReviewSerializer(instance=review)
    movie_data = serializer.data

    assert movie_data["id"] == review.id
    assert movie_data["user"] == users[0].username
    assert movie_data["rating"] == review.rating
    assert movie_data["review"] == review.review
    assert movie_data["created_at"] == review.created_at
