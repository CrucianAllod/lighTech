import logging

from django.core.cache import cache
from django.db import transaction

from balance.models import Balance, BalanceOperation, OperationType

logger = logging.getLogger(__name__)

class BalanceService:
    @staticmethod
    def deposit(user: Balance.user, deposit_amount: float) -> Balance:
        logger.info(f"Пополнение баланса пользователя {user.id} на сумму {deposit_amount}")
        try:
            balance = user.balance
            with transaction.atomic():
                balance.amount += deposit_amount
                balance.save()

                BalanceOperation.objects.create(
                    balance=balance,
                    related_balance=None,
                    operation=OperationType.DEPOSIT,
                    operation_amount=deposit_amount,
                    operation_result=balance.amount
                )
            cache.delete(f'balance_operations_user_{user.id}')
            logger.info(f"Успешное пополнение баланса пользователя {user.id}. Новый баланс: {balance.amount}")
        except Exception as e:
            logger.error(f"Ошибка при пополнении баланса: {e}", exc_info=True)
            raise

        return balance

    @staticmethod
    def withdraw(user: Balance.user, withdraw_amount: float) -> Balance:
        logger.info(f"Начинается снятие со счета пользователя {user.id} на сумму {withdraw_amount}")
        try:
            balance = user.balance
            if balance.amount < withdraw_amount:
                logger.warning(f"Попытка снятия {withdraw_amount} с недостаточным балансом у пользователя {user.id} (текущий баланс: {balance.amount})")
                raise ValueError('Недостаточно средств на балансе.')

            with transaction.atomic():
                balance.amount -= withdraw_amount
                balance.save()

                BalanceOperation.objects.create(
                    balance=balance,
                    related_balance=None,
                    operation=OperationType.WITHDRAW,
                    operation_amount=withdraw_amount,
                    operation_result=balance.amount
                )
            cache.delete(f'balance_operations_user_{user.id}')
            logger.info(f"Успешное снятие со счета пользователя {user.id}. Новый баланс: {balance.amount}")
        except Exception as e:
            logger.error(f"Ошибка при пополнении баланса: {e}", exc_info=True)
            raise

        return balance

    @staticmethod
    def transfer(user_out: Balance.user, balance_in_id: Balance, amount_transfer: float) -> Balance:
        logger.info(f"Начинается перевод {amount_transfer} от пользователя {user_out.id} к балансу {balance_in_id}")
        try:
            balance_out = user_out.balance
            balance_in = Balance.objects.get(id=balance_in_id)
            if amount_transfer <= 0:
                logger.warning(f"Пользователь {user_out.id} попытался перевести невалидную сумму {amount_transfer}")
                raise ValueError('Сумма перевода должна быть положительной.')
            if balance_out.user_id == balance_in.user_id:
                logger.warning(f"Пользователь {user_out.id} попытался сделать перевод себе самому")
                raise ValueError('Нельзя переводить средства самому себе.')
            if balance_out.amount < amount_transfer:
                logger.warning(f"Пользователь {user_out.id} попытался перевести {amount_transfer}, но недостаточно средств (текущий баланс: {balance_out.amount})")
                raise ValueError('Недостаточно средств на балансе.')

            with transaction.atomic():
                balance_out.amount -= amount_transfer
                balance_out.save()

                balance_in.amount += amount_transfer
                balance_in.save()

                BalanceOperation.objects.create(
                    balance=balance_out,
                    related_balance=balance_in,
                    operation=OperationType.TRANSFER_OUT,
                    operation_amount=amount_transfer,
                    operation_result=balance_out.amount,
                )

                BalanceOperation.objects.create(
                    balance=balance_in,
                    related_balance=balance_out,
                    operation=OperationType.TRANSFER_IN,
                    operation_amount=amount_transfer,
                    operation_result=balance_in.amount,
                )
            cache.delete(f'balance_operations_user_{user_out.id}')
            cache.delete(f'balance_operations_user_{balance_in.user_id}')
            logger.info(f"Успешный перевод {amount_transfer} от пользователя {user_out.id} к пользователю {balance_in.user_id}")
        except Exception as e:
            logger.error(
                f"Ошибка при переводе {amount_transfer} от пользователя {user_out.id} к балансу {balance_in_id}: {e}",
                exc_info=True)
            raise

        return balance_out