from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from statuses.models import Status
from tasks.filters import TaskFilter
from tasks.models import Task

User = get_user_model()


class TestTask(TestCase):
    fixtures = ['dbdump.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='anton', password='asdf7jkl')
        self.author = User.objects.get(username='anton')
        self.executor = User.objects.get(username='test')
        self.status = Status.objects.get(name='New Status')

    def test_create_task(self):
        self.response = self.client.post(
            reverse_lazy('create_task'),
            data={
                'name': 'Created task',
                'description': 'This is task description',
                'author': self.author.pk,
                'executor': self.executor.pk,
                'status': self.status.pk,
            }
        )
        task = Task.objects.select_related('author', 'executor').\
            get(name='Created task')

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertTrue(task)
        self.assertEqual(self.author, task.author)
        self.assertEqual(self.executor, task.executor)

    def test_update_task(self):
        task = Task.objects.get(name='test task')
        self.response = self.client.post(
            reverse_lazy('update_task', kwargs={'pk': task.pk}),
            data={
                'name': 'Test task updated',
                'description': 'Updated task',
                'author': self.author.id,
                'executor': self.executor.id,
                'status': self.status.id,
            }
        )

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertTrue(Task.objects.get(name='Test task updated'))

    def test_delete_task(self):
        self.client.login()
        task = Task.objects.get(name='For deleted')
        self.response = self.client.post(
            reverse_lazy('delete_task', kwargs={'pk': task.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertFalse(Task.objects.filter(name='For deleted'))
        self.client.post(reverse_lazy('delete_task', kwargs={'pk': 5}))
        self.assertTrue(Task.objects.filter(pk=5))

    def test_filter_task(self):
        qs = Task.objects.all()
        f = TaskFilter(
            data={'executor': 12},
            queryset=qs
        )
        filtered_tasks = f.qs.order_by('id')
        expected_tasks = Task.objects.filter(executor=12).order_by('id')
        self.assertQuerysetEqual(filtered_tasks, expected_tasks)
