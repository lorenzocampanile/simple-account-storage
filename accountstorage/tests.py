from django.test import TestCase, Client
from authentication.models import User
from accountstorage.models import Account


class AccountListSecurityTestCase(TestCase):
    EXAMPLE_USERNAME_01 = 'user01'
    EXAMPLE_USERNAME_01_ACCOUNT_NAME = 'user01account'

    EXAMPLE_USERNAME_02 = 'user02'
    EXAMPLE_USERNAME_02_ACCOUNT_NAME = 'user02account'

    EXAMPLE_LINK = 'https://google.it'
    EXAMPLE_PASSWORD = 'test'

    def setUp(self):
        """Creates two differet users associated to two different accounts."""
        user01 = User.objects.create_user(username=self.EXAMPLE_USERNAME_01,
            password=self.EXAMPLE_PASSWORD)
        Account.objects.create(user=user01,
            label=self.EXAMPLE_USERNAME_01_ACCOUNT_NAME, username='01',
            link=self.EXAMPLE_LINK, notes='', password=self.EXAMPLE_PASSWORD)

        user02 = User.objects.create_user(username=self.EXAMPLE_USERNAME_02,
            password=self.EXAMPLE_PASSWORD)
        Account.objects.create(user=user02,
            label=self.EXAMPLE_USERNAME_02_ACCOUNT_NAME, username='02',
            link=self.EXAMPLE_LINK, notes='', password=self.EXAMPLE_PASSWORD)

    def test_authentication_required_on_accounts_list_page(self):
        """
        Ensure that the accounts list page is visible only when the user is
        authenticated.
        """
        response = self.client.get('/accounts/')
        self.assertEqual(302, response.status_code)

    def test_user_can_see_only_its_accounts(self):
        """
        Ensure that the user can only see its accouns.
        """
        self.client.login(username=self.EXAMPLE_USERNAME_01,
            password=self.EXAMPLE_PASSWORD)

        user01 = User.objects.get(username=self.EXAMPLE_USERNAME_01)
        response = self.client.get('/accounts/')
        for account in response.context.get('object_list', []):
            self.assertTrue(account.user == user01)
