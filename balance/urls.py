from django.urls import path

from balance.views.deposit_view import BalanceDepositAPIView
from balance.views.operation_view import OperationListAPIView
from balance.views.transfer_view import BalanceTransferAPIView
from balance.views.withdraw_view import BalanceWithdrawAPIView

urlpatterns = [
    path('deposit/', BalanceDepositAPIView.as_view(), name='deposit'),
    path('withdraw/', BalanceWithdrawAPIView.as_view(), name='withdraw'),
    path('transfer/', BalanceTransferAPIView.as_view(), name='transfer'),
    path('operations/', OperationListAPIView.as_view(), name='operations'),
]