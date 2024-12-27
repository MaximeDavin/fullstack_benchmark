from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    description = models.TextField()
    released_at = models.DateField()
    cover_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.year})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_review")
        ]

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username} - Rating: {self.rating}"
