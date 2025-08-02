from django.db import transaction

from balance.models import Balance, BalanceOperation, OperationType


class BalanceService:
    @staticmethod
    def create_deposit(balance: Balance, deposit_amount: float) -> Balance:
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
        return balance

    @staticmethod
    def create_withdraw(balance: Balance, withdraw_amount: float) -> Balance:

        if balance.amount < withdraw_amount:
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
        return balance

    @staticmethod
    def create_transfer(balance_out: Balance, balance_in: Balance, amount_transfer: float) -> Balance:

        if amount_transfer <= 0:
            raise ValueError('Сумма перевода должна быть положительной.')
        if balance_out.user_id == balance_in.user_id:
            raise ValueError('Нельзя переводить средства самому себе.')
        if balance_out.amount < amount_transfer:
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
        return balance_out