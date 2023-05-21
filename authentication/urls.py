from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView


app_name = "authentication"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
]
