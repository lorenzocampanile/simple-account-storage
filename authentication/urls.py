from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path('encryption-keys/', views.RetrieveEncryptionKeysView.as_view(), name='retrieve_encryption_keys'),
]
