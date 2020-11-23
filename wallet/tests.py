from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

import ddt

from . import models


class SigninTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com')
        self.user.save()
    def tearDown(self):
        self.user.delete()
    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)
    def test_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


@ddt.ddt
class AccountTestCase(TestCase):

    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com')
        self.user.save()
        self.client = Client()
        self.client.login(username='test', password='12test12')

    def test_account_created_redirect_to_all_accounts(self):
        response = self.client.post(
            '/wallet/account/create/',
            {'name': 'testname',
             'balance': '100',
             'user': self.user}
        )
        self.assertEqual(response.url, reverse('wallet:all_accounts'))

    def test_create_one_account(self):
        self.client.post(
            '/wallet/account/create/',
            {'name': 'testname',
             'balance': '100'}
        )
        models.Account.objects.get()

    @ddt.data('slug1', 'slug2')
    def test_slug_created(self, title):
        self.client.post(
            '/wallet/account/create/',
            {'name': title,
             'balance': '100'}
        )
        account = models.Account.objects.get()
        self.assertEqual(account.slug, title)

    @ddt.data(
        ('sl ug1', 'sl-ug1'),
        ('Дом', 'dom'),
        ('оплата счетов', 'oplata-schetov')
    )
    @ddt.unpack
    def test_slug_created_correctly(self, title, expected_slug):
        self.client.post(
            '/wallet/account/create/',
            {'name': title,
             'balance': '100'}
        )
        account = models.Account.objects.get()
        self.assertEqual(account.slug, expected_slug)
