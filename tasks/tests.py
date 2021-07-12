from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class TestUser(TestCase):
    fixtures = ['dbdump.json']

    def setUp(self):
        self.client = Client()

    def test_user_create(self):
        self.response = self.client.post(
            reverse_lazy('register'),
            data={
                'first_name': 'Anton',
                'last_name': 'Semenov',
                'username': 'zavr',
                'password1': 'asdf7jkl',
                'password2': 'asdf7jkl',
            }
        )
        self.assertRedirects(self.response, reverse_lazy('login'))
        self.assertTrue(User.objects.get(
            username='zavr',
            first_name='Anton',
            last_name='Semenov'
        ))

    def test_update_user(self):
        self.client.login(username='test', password='asdf9jkl')
        user = User.objects.get(username='test')
        self.response = self.client.post(
            reverse_lazy('change_user', kwargs={'pk': user.pk}),
            data={
                'username': 'ant',
                'first_name': 'Anton',
                'last_name': 'Semenov',
                'password1': 'asdf7jkl',
                'password2': 'asdf7jkl',
            }
        )
        self.assertRedirects(self.response, reverse_lazy('user_list'))
        self.assertTrue(User.objects.get(username='ant'))

    def test_delete_user(self):
        self.client.login(username='test', password='asdf9jkl')
        user = User.objects.get(username='test')
        self.response = self.client.post(
            reverse_lazy('delete_user', kwargs={'pk': user.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('user_list'))
        self.assertFalse(User.objects.filter(username='test'))
