import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from balance.models import Balance

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username="user1", password="pass")
    Balance.objects.create(user=user, amount=1000)
    return user

@pytest.fixture
def second_user(db):
    second_user = User.objects.create_user(username="user2", password="pass")
    Balance.objects.create(user=second_user, amount=500)
    return second_user