from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.permissions import IsOwner

from .models import Movie, Review
from .serializers import (
    DetailMovieSerializer,
    ListMovieSerializer,
    ReadReviewSerializer,
    ReviewSerializer,
)


class MovieViewSet(ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["year"]
    ordering_fields = [
        "released_at",
        "title",
    ]
    ordering = ["released_at", "title"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListMovieSerializer
        return DetailMovieSerializer

    def get_queryset(self):
        if self.action == "list":
            return Movie.objects.all()
        return Movie.objects.prefetch_related(
            Prefetch("review_set", queryset=Review.objects.select_related("user"))
        )


class ReviewViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["movie", "user"]
    ordering_fields = [
        "created_at",
        "rating",
    ]
    ordering = ["created_at"]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadReviewSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwner()]
        return []

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        """
        Automatically set the user field to the user making the request.
        """
        serializer.save(user=self.request.user)
