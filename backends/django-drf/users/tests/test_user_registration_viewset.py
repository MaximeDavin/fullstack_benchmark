import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user_successful(api_client):
    data = {"username": "testuser123", "password": "strongpassword"}
    response = api_client.post(reverse("register-user"), data)
    assert response.status_code == 201
    assert User.objects.filter(username="testuser123").exists()


def test_register_user_invalid_data(api_client):
    data = {"username": "short", "password": "123"}
    response = api_client.post(reverse("register-user"), data)
    assert response.status_code == 400
    assert "username" in response.data
    assert "password" in response.data


# Ensure the endpoint is accessible without authentication
def test_register_user_permission(api_client):
    response = api_client.options(reverse("register-user"))
    assert response.status_code == 200
