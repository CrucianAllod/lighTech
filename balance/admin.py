from django.contrib import admin

from balance.models import Balance, BalanceOperation

admin.site.register(Balance)
admin.site.register(BalanceOperation)