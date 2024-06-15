from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.views import APIView


class RetrieveEncryptionKeysView(APIView):
    permission_classes  = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response({
            'public_key': request.user.public_key,
            'encrypted_private_key': request.user.encrypted_private_key,
        })
