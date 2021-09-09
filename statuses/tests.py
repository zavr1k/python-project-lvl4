from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

from .models import Status


class TestStatus(TestCase):
    fixtures = ['statuses_dump.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='asdf9jkl')

    def test_create_status(self):
        self.response = self.client.post(
            reverse_lazy('create_status'),
            data={'name': 'New status'}
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertTrue(Status.objects.get(name='New status'))

    def test_update_status(self):
        status = Status.objects.get(name='Old status')
        self.response = self.client.post(
            reverse_lazy('update_status', kwargs={'pk': status.pk}),
            data={'name': 'Updated status'}
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertEqual(
            Status.objects.get(name='Updated status').pk, status.pk)

    def test_delete_status(self):
        status = Status.objects.get(name='For delete')
        self.response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': status.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('status_list'))
        self.assertFalse(Status.objects.filter(name='For delete'))
