from django.test import TestCase
from django.urls import reverse
from .models import Wallet


class WalletTests(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create()

    def test_balance_increase(self):
        response = self.client.post(
            reverse('wallet-operation', args=[str(self.wallet.uuid)]),
            data={'operation_type': 'DEPOSIT', 'amount': 100.00}
        )
        self.assertEqual(response.status_code, 200)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 100.00)

    def test_balance_decrease(self):
        self.wallet.balance = 100
        self.wallet.save()
        response = self.client.post(
            reverse('wallet-operation', args=[str(self.wallet.uuid)]),
            data={'operation_type': 'WITHDRAW', 'amount': 50}
        )
        self.assertEqual(response.status_code, 200)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 50)

    def test_insufficient_funds(self):
        self.wallet.balance = 50
        self.wallet.save()
        response = self.client.post(
            reverse('wallet-operation', args=[str(self.wallet.uuid)]),
            data={'operation_type': 'WITHDRAW', 'amount': 100}
        )
        self.assertEqual(response.status_code, 400)
