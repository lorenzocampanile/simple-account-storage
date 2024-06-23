from typing import Any

from django.db.models.query import QuerySet, Q
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accountstorage.encrypt import decrypt_password
from accountstorage.models import Account
from .serializers import AccountSerializer


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        return Account.objects.prefetch_related('web', 'ssh', 'db')\
                              .filter(user=self.request.user)\
                              .order_by('label')


class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) -> QuerySet[Any]:
        base_query = Account.objects.prefetch_related('web', 'ssh', 'db')\
                                    .filter(user=self.request.user)\
                                    .order_by('label')

        return self._apply_query_filters(qs=base_query)

    def _apply_query_filters(self, qs: QuerySet[Account]) -> QuerySet[Account]:
        if account_type := self.request.GET.get('type'):
            qs = qs.filter(type=account_type)

        if search_text := self.request.GET.get('search'):
            qs = qs.filter(
               Q(label__icontains=search_text) |
               Q(username__icontains=search_text) |
               Q(notes__icontains=search_text) |
               Q(web__link__icontains=search_text) |
               Q(ssh__host__icontains=search_text) |
               Q(db__host__icontains=search_text) |
               Q(db__type__icontains=search_text)
            )

        return qs
