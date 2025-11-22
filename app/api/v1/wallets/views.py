from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Wallet
from .serializers import WalletSerializer

import threading


lock = threading.Lock()


class WalletOperationView(APIView):
    def post(self, request, wallet_uuid):
        operation_type = request.data.get("operation_type")
        amount = request.data.get("amount")
        if operation_type not in ["DEPOSIT", "WITHDRAW"]:
            return Response({"error": "Invalid operation_type"}, status=status.HTTP_400_BAD_REQUEST)
        if amount is None or amount <= 0:
            return Response({"error": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                wallet = get_object_or_404(Wallet, pk=wallet_uuid)
                lock.acquire()
                wallet = Wallet.objects.select_for_update().get(pk=wallet_uuid)

                new_balance = wallet.balance
                if operation_type == "DEPOSIT":
                    new_balance += amount
                elif operation_type == "WITHDRAW":
                    if wallet.balance < amount:
                        return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
                    new_balance -= amount
                wallet.balance = new_balance
                wallet.save()
            return Response({"balance": str(wallet.balance)})
        finally:
            lock.release()


class WalletBalanceView(APIView):
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, pk=wallet_uuid)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

