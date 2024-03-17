from django.urls import path

from rest_framework.routers import DefaultRouter

from accountstorage.views import AccountListView, AccountViewSet


app_name = "account"
urlpatterns = []

router = DefaultRouter()
router.register(r'', AccountViewSet, basename='accounts')
urlpatterns = router.urls
