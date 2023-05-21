from django.contrib import admin
from accountstorage.models import Account, WebAccount, SSHAccount, DatabaseAccount


class WebAccountInline(admin.TabularInline):
    model = WebAccount


class SSHAccountInline(admin.TabularInline):
    model = SSHAccount


class DatabaseAccountInline(admin.TabularInline):
    model = DatabaseAccount


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [
        WebAccountInline,
        SSHAccountInline,
        DatabaseAccountInline,
    ]
