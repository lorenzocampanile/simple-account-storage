from typing import Any

from django.db.models.query import QuerySet
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
        return Account.objects.prefetch_related('web', 'ssh', 'db')\
                              .filter(user=self.request.user)\
                              .order_by('label')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data

        # Decode the password using the encryption key
        encryption_key = request.META['HTTP_X_ENCRYPTION_KEY']
        plain_text_password = decrypt_password(instance.password, encryption_key)
        response_data['password'] = plain_text_password

        return Response(response_data)
