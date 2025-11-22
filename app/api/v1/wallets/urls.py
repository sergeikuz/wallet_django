from django.urls import path
from .views import WalletOperationView, WalletBalanceView

urlpatterns = [
    path('<uuid:wallet_uuid>/operation/', WalletOperationView.as_view()),
    path('<uuid:wallet_uuid>/', WalletBalanceView.as_view()),
]