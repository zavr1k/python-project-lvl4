from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from tasks.models import TaskStatus, Task

User = get_user_model()


class TestUser(TestCase):
    fixtures = ['dbdump.json', ]

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
        self.client.login(username='withoutreq', password='asdf7jkl;')
        user = User.objects.get(username='withoutreq')
        self.response = self.client.post(
            reverse_lazy('delete_user', kwargs={'pk': user.id})
        )

        self.assertRedirects(self.response, reverse_lazy('user_list'))
        self.assertFalse(User.objects.filter(username='withoutreq'))


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


class TestTask(TestCase):
    fixtures = ['dbdump.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='anton', password='asdf7jkl')
        self.author = User.objects.get(username='anton')
        self.executor = User.objects.get(username='test')
        self.status = TaskStatus.objects.get(title='New Status')

    def test_create_task(self):
        self.response = self.client.post(
            reverse_lazy('create_task'),
            data={
                'title': 'Created task',
                'description': 'This is task description',
                'author': self.author.pk,
                'executor': self.executor.pk,
                'status': self.status.pk,
            }
        )
        task = Task.objects.select_related('author', 'executor').\
            get(title='Created task')

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertTrue(task)
        self.assertEqual(self.author, task.author)
        self.assertEqual(self.executor, task.executor)

    def test_update_task(self):
        task = Task.objects.get(title='test task')
        self.response = self.client.post(
            reverse_lazy('update_task', kwargs={'pk': task.pk}),
            data={
                'title': 'Test task updated',
                'description': 'Updated task',
                'author': self.author.id,
                'executor': self.executor.id,
                'status': self.status.id,
            }
        )

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertTrue(Task.objects.get(title='Test task updated'))

    def test_delete_task(self):
        self.client.login()
        task = Task.objects.get(title='For deleted')
        self.response = self.client.post(
            reverse_lazy('delete_task', kwargs={'pk': task.pk})
        )

        self.assertRedirects(self.response, reverse_lazy('task_list'))
        self.assertFalse(Task.objects.filter(title='For deleted'))
        self.client.post(reverse_lazy('delete_task', kwargs={'pk': 5}))
        self.assertTrue(Task.objects.filter(pk=5))
