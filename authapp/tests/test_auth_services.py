import pytest
from django.contrib.auth.models import User
from unittest.mock import patch

from authapp.services import AuthService

@pytest.mark.django_db
def test_register_user_success():
    user = AuthService.register_user(username="testuser", password="secret", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert hasattr(user, 'balance')
    assert user.balance is not None
    assert user.balance.user == user

@pytest.mark.django_db
def test_register_user_duplicate_username():
    User.objects.create_user(username="existinguser", password="secret")
    with pytest.raises(ValueError) as exc_info:
        AuthService.register_user(username="existinguser", password="secret")
    assert "уже существует" in str(exc_info.value)

@pytest.mark.django_db
def test_register_user_unexpected_exception():
    with patch('django.contrib.auth.models.User.objects.create_user') as mock_create_user:
        mock_create_user.side_effect = Exception("Some unexpected error")
        with pytest.raises(Exception) as exc_info:
            AuthService.register_user(username="anyuser", password="secret")
        assert "Some unexpected error" in str(exc_info.value)
