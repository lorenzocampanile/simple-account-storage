from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from accountstorage.models import Account


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        return Account.objects.prefetch_related('web', 'ssh', 'db')\
                              .filter(user=self.request.user)\
                              .order_by('label')
