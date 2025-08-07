import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user