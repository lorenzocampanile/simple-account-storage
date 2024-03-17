from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from rest_framework import status
