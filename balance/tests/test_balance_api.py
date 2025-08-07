import pytest
from rest_framework import status
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize("url_name, payload, expected_status", [
    ("balance-deposit", {"amount": 100}, status.HTTP_200_OK),
    ("balance-deposit", {"amount": 0}, status.HTTP_400_BAD_REQUEST),
    ("balance-withdraw", {"amount": 300}, status.HTTP_200_OK),
    ("balance-withdraw", {"amount": 1500}, status.HTTP_400_BAD_REQUEST),
])
def test_deposit_withdraw(api_client, user, url_name, payload, expected_status):
    api_client.force_authenticate(user=user)
    url = reverse(url_name)
    response = api_client.post(url, payload)
    assert response.status_code == expected_status

@pytest.mark.django_db
def test_transfer(api_client, user, second_user):
    api_client.force_authenticate(user=user)
    url = reverse("balance-transfer")
    data = {"amount": 200, "balance_in": second_user.balance.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_transfer_fail_to_self(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("balance-transfer")
    data = {"amount": 100, "balance_in": user.balance.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "самому себе" in response.data.get("error", "").lower()

@pytest.mark.django_db
def test_operations_auth_required(api_client):
    url = reverse("balance-operations")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
