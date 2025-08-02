from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from balance.models import Balance, BalanceOperation

User = get_user_model()

class BalanceTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1', password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='password2'
        )

        cls.balance1 = Balance.objects.create(user=cls.user1, amount=1000)
        cls.balance2 = Balance.objects.create(user=cls.user2, amount=500)

    def setUp(self):
        self.client.force_authenticate(user=self.user1)
        self.deposit_url = '/api/balance/v1/deposit/'
        self.withdraw_url = '/api/balance/v1/withdraw/'
        self.transfer_url = '/api/balance/v1/transfer/'
        self.operations_url = '/api/balance/v1/operations/'

    def test_deposit_funds(self):
        data = {'amount': 500}
        response = self.client.post(self.deposit_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.balance1.refresh_from_db()
        self.assertEqual(self.balance1.amount, 1500)
        self.assertTrue(
            BalanceOperation.objects.filter(
                balance=self.balance1,
                operation='deposit',
                operation_amount=500
            ).exists()
        )

    def test_withdraw_funds(self):
        data = {'amount': 300}
        response = self.client.post(self.withdraw_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.balance1.refresh_from_db()
        self.assertEqual(self.balance1.amount, 700)
        self.assertTrue(
            BalanceOperation.objects.filter(
                balance=self.balance1,
                operation='withdraw',
                operation_amount=300
            ).exists()
        )

    def test_insufficient_funds_withdraw(self):
        data = {'amount': 1500}
        response = self.client.post(self.withdraw_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_transfer_funds(self):
        data = {'amount': 200, 'balance_in': self.balance2.id}
        response = self.client.post(self.transfer_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.balance1.refresh_from_db()
        self.balance2.refresh_from_db()
        self.assertEqual(self.balance1.amount, 800)
        self.assertEqual(self.balance2.amount, 700)

        self.assertTrue(
            BalanceOperation.objects.filter(
                balance=self.balance1,
                operation='transfer_out',
                operation_amount=200
            ).exists()
        )
        self.assertTrue(
            BalanceOperation.objects.filter(
                balance=self.balance2,
                operation='transfer_in',
                operation_amount=200
            ).exists()
        )

    def test_operations_history(self):
        BalanceOperation.objects.create(
            balance=self.balance1,
            operation='deposit',
            operation_amount=1000,
            operation_result=1000
        )
        response = self.client.get(self.operations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['operation_amount'], '1000.00')