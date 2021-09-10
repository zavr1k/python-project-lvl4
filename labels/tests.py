from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy

from .models import Label


class TestLabel(TestCase):
    fixtures = ['labels_dump.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username='test', password='asdf9jkl')

    def test_label_creation(self):
        self.response = self.client.post(
            reverse_lazy('create_label'),
            data={'name': 'New label'}
        )

        self.assertRedirects(self.response, reverse_lazy('label_list'))
        self.assertTrue(Label.objects.get(name='New label'))

    def test_label_update(self):
        label = Label.objects.get(name='Exist label')
        self.response = self.client.post(
            reverse_lazy('update_label', kwargs={'pk': label.pk}),
            data={'name': 'Updated'}
        )

        self.assertRedirects(self.response, reverse_lazy('label_list'))
        self.assertTrue(Label.objects.get(name='Updated'))

    def test_label_delete(self):
        label = Label.objects.get(name='For delete')
        self.response = self.client.post(
            reverse_lazy('delete_label', kwargs={'pk': label.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('label_list'))
        self.assertFalse(Label.objects.filter(name='For delete'))
        self.client.post(reverse_lazy('update_label', kwargs={'pk': 1}))
        self.assertTrue(Label.objects.filter(pk=1))
