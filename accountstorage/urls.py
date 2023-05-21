from django.urls import path
from accountstorage.views import AccountListView

app_name = "account"
urlpatterns = [
    path('', AccountListView.as_view(), name='index'),
]
