from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from tasks.models import TaskStatus


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


class TestStatus(TestCase):

    fixtures = ['dbdump.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='asdf9jkl')

    def test_create_status(self):
        self.response = self.client.post(
            reverse_lazy('create_status'),
            data={'title': 'New status'}
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertTrue(TaskStatus.objects.get(title='New status'))

    def test_update_status(self):
        status = TaskStatus.objects.get(title='Old status')
        self.response = self.client.post(
            reverse_lazy('update_status', kwargs={'pk': status.pk}),
            data={'title': 'Updated status'}
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertEqual(
            TaskStatus.objects.get(title='Updated status').pk, status.pk)

    def test_delete_status(self):
        status = TaskStatus.objects.get(title='For delete')
        self.response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': status.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertFalse(TaskStatus.objects.filter(title='For delete'))
