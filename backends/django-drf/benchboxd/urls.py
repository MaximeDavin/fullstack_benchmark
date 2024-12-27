from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.views import MovieViewSet, ReviewViewSet
from users.views import RegisterUserViewSet

from .views import reset

router = SimpleRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"reviews", ReviewViewSet, basename="review")


urlpatterns = [
    path(
        "register/",
        RegisterUserViewSet.as_view({"post": "create"}),
        name="register-user",
    ),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-user"),
    path("reset/", reset, name="reset"),
    *router.urls,
]
