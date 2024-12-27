from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth.models import User

from ..models import Movie, Review


@pytest.fixture(scope="session")
def movie_data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        users = User.objects.bulk_create(
            [User(username=f"username {i}") for i in range(6)]
        )

        movie1 = Movie.objects.create(
            id="inception",
            title="Inception",
            year=2010,
            description="A mind-bending thriller",
            released_at="2010-07-16",
            cover_path="/cover1.png",
        )
        movie2 = Movie.objects.create(
            id="the-matrix",
            title="The Matrix",
            year=1999,
            description="A hacker discovers the truth about his reality.",
            released_at="1999-03-31",
            cover_path="/cover2.png",
        )
        movie3 = Movie.objects.create(
            id="the-godfather",
            title="The Godfather",
            year=1972,
            description="A chronicle of the fictional Italian-American Corleone crime family.",
            released_at="1972-03-15",
            cover_path="/cover3.png",
        )

        reviews = Review.objects.bulk_create(
            [
                Review(
                    user=users[i],
                    movie=movie1,
                    rating=i % 5,
                    review=f"Review content {i}",
                )
                for i in range(6)
            ]
            + [
                Review(
                    user=users[i],
                    movie=movie2,
                    rating=i % 5,
                    review=f"Review content {i}",
                )
                for i in range(6)
            ]
        )

        # We update created_at so we can test we order by most recent review
        base_date = datetime(year=2024, month=12, day=1, tzinfo=ZoneInfo("UTC"))
        for i, review in enumerate(reviews):
            review.created_at = base_date.replace(hour=i).isoformat()
        Review.objects.bulk_update(reviews, ["created_at"])

        yield (movie1, movie2, movie3), reviews, users

        Review.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
