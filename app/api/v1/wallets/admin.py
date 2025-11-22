from django.contrib import admin
from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "balance", "uuid")
    list_filter = ("id", "balance", "uuid")
    search_fields = ("uuid",)
