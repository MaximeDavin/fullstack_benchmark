import pytest
from django.contrib.auth.models import User

from ..serializers import UserSerializer


def test_user_serializer_valid_data():
    data = {"username": "testuser123", "password": "strongpassword"}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


def test_user_serializer_invalid_username_length():
    data = {"username": "short", "password": "strongpassword"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors


def test_user_serializer_invalid_password_length():
    data = {"username": "testuser123", "password": "short"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_user_serializer_create():
    data = {"username": "testuser123", "password": "strongpassword"}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert isinstance(user, User)
    assert user.username == "testuser123"
    assert user.check_password("strongpassword")
