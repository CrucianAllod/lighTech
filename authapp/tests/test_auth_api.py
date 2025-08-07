import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
def test_register_success(api_client):
    data = {
        'username': 'newuser',
        'password': 'newpassword123',
        'confirm_password': 'newpassword123'
    }
    response = api_client.post('/api/auth/v1/register/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
@pytest.mark.parametrize("data, error_field", [
    ({'username': 'user', 'password': 'pass', 'confirm_password': 'wrong'}, 'password'),
    ({'username': '', 'password': 'pass', 'confirm_password': 'pass'}, 'username'),
])
def test_register_validation_errors(api_client, data, error_field):
    response = api_client.post('/api/auth/v1/register/', data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_field in response.data

@pytest.mark.django_db
def test_login_success(api_client, test_user):
    data = {'username': test_user.username, 'password': 'testpassword'}
    response = api_client.post('/api/auth/v1/login/', data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_fail_wrong_password(api_client, test_user):
    data = {'username': test_user.username, 'password': 'wrongpassword'}
    response = api_client.post('/api/auth/v1/login/', data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST or status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_success(api_client, test_user):
    refresh = RefreshToken.for_user(test_user)
    api_client.force_authenticate(user=test_user)
    data = {'refresh_token': str(refresh)}

    response = api_client.post('/api/auth/v1/logout/', data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('success') == 'Выход успешен'

@pytest.mark.django_db
def test_logout_fail_invalid_token(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    data = {'refresh_token': 'invalidtoken'}

    response = api_client.post('/api/auth/v1/logout/', data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data
