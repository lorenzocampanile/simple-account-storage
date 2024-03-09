from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from rest_framework import status


class ApiLoginView(LoginView):
    """
    Default Django LoginView with some little customizations to make it
    suitable for REST APIs contexts.
    """
    def form_valid(self, form):
        """If the form is valid, return 200 OK code."""
        auth_login(self.request, form.get_user())
        return HttpResponse(status=status.HTTP_200_OK)

    def form_invalid(self, form):
        """If the form is invalid, return 401 Unauthorized code."""
        print(form.errors)
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
