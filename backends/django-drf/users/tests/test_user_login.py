import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user_successful():
    User.objects.create_user(username="testuser123", password="strongpassword")
    api_client = APIClient()
    data = {"username": "testuser123", "password": "strongpassword"}
    response = api_client.post(reverse("login-user"), data)
    assert response.status_code == 200
    assert "access" in response.json()
