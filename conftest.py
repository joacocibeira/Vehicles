import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture()
def user(db):
    user = User.objects.create_user(username="test_user", password="test_password")
    return user


@pytest.fixture()
def api_client(user):
    client = APIClient()
    return client
