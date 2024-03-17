from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from .views import ApiLoginView


app_name = "authentication"
urlpatterns = [
]
