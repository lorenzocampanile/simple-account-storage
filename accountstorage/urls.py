from django.urls import path

from rest_framework.routers import DefaultRouter

from accountstorage.views import AccountListView, AccountViewSet


app_name = "account"
urlpatterns = [
    path('', AccountListView.as_view(), name='index'),
]

router = DefaultRouter()
router.register(r'api', AccountViewSet, basename='accounts')
urlpatterns = router.urls
