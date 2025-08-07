import pytest
from unittest.mock import patch
from balance.services import BalanceService

@pytest.mark.django_db
def test_deposit_increases_balance(user):
    user.balance.amount = 100
    user.balance.save()
    new_balance = BalanceService.deposit(user, 50)
    assert new_balance.amount == 150

@pytest.mark.django_db
def test_withdraw_insufficient_funds_raises(user):
    user.balance.amount = 50
    user.balance.save()
    with pytest.raises(ValueError):
        BalanceService.withdraw(user, 100)

@pytest.mark.django_db
def test_transfer_to_self_raises(user):
    user.balance.amount = 100
    user.balance.save()
    with pytest.raises(ValueError):
        BalanceService.transfer(user, user.balance.id, 50)

@pytest.mark.django_db
@patch("balance.services.cache")
def test_cache_cleared_after_deposit(mock_cache, user):
    user.balance.amount = 100
    user.balance.save()
    BalanceService.deposit(user, 50)
    mock_cache.delete.assert_called_with(f"balance_operations_user_{user.id}")
