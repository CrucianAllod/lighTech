from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Баланс пользователя"
        verbose_name_plural = "Балансы пользователей"
        ordering = ['user']

    def __str__(self):
        return f"Баланс пользователя {self.user.username}: {self.amount}"

class OperationType(models.TextChoices):
    DEPOSIT = 'deposit', 'Пополнение'
    WITHDRAW = 'withdraw', 'Списание'
    TRANSFER_IN = 'transfer_in', 'Перевод на счет'
    TRANSFER_OUT = 'transfer_out', 'Перевод со счета'

class BalanceOperation(models.Model):

    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='operations')
    related_balance = models.ForeignKey(Balance, null=True, blank=True, on_delete=models.SET_NULL, related_name='related_operations')
    operation = models.CharField(max_length=20, choices=OperationType.choices)
    operation_amount = models.DecimalField(max_digits=12, decimal_places=2)
    operation_result = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Операция с балансом"
        verbose_name_plural = "Операции с балансом"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_operation_display()} {self.operation_amount} => {self.operation_result} at {self.created_at}"