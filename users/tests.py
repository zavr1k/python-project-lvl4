from django.test import TestCase, Client
from django.urls import reverse_lazy

from .models import TaskUser


class TestUser(TestCase):
    fixtures = ['users_dump.json', ]

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
        self.assertTrue(TaskUser.objects.get(
            username='zavr',
            first_name='Anton',
            last_name='Semenov'
        ))

    def test_update_user(self):
        self.client.login(username='test', password='asdf9jkl')
        user = TaskUser.objects.get(username='test')
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
        self.assertRedirects(self.response, reverse_lazy('users'))
        self.assertTrue(TaskUser.objects.get(username='ant'))

    def test_delete_user(self):
        self.client.login(username='withoutreq', password='asdf7jkl')
        user = TaskUser.objects.get(username='withoutreq')
        self.response = self.client.post(
            reverse_lazy('delete_user', kwargs={'pk': user.id})
        )

        self.assertRedirects(self.response, reverse_lazy('users'))
        self.assertFalse(TaskUser.objects.filter(username='withoutreq'))
