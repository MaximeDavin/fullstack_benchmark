import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_reset():
    User.objects.create_user(username="testuser123", password="strongpassword")
    assert User.objects.count() != 0

    client = APIClient()
    response = client.post(reverse("reset"))
    assert response.status_code == 204
    assert User.objects.count() == 0
