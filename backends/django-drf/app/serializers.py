from rest_framework import serializers

from .models import Movie, Review


class ListMovieSerializer(serializers.ModelSerializer):
    """Read only Movie serializer used in the list view"""

    class Meta:
        model = Movie
        fields = ("id", "title", "year", "description", "released_at", "cover_path")
        read_only_fields = fields


class DetailMovieSerializer(serializers.ModelSerializer):
    """Read only Movie serializer used in the detail view that
    add a list of 5 reviews"""

    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "year",
            "description",
            "released_at",
            "cover_path",
            "reviews",
        )
        read_only_fields = fields

    def get_reviews(self, movie):
        reviews = movie.review_set.order_by("-created_at")[
            :5
        ]  # Get the latest 5 reviews for the movie
        # reviews = Review.objects.filter(movie=movie).order_by('-created_at')[:5]  # Get the latest 5 reviews for the movie
        return ReadReviewSerializer(reviews, many=True, read_only=True).data


class ReadReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "movie",
            "rating",
            "review",
            "created_at",
        )
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "movie",
            "rating",
            "review",
            "created_at",
        )
        read_only_fields = (
            "id",
            "user",
        )
