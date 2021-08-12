from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from tasks.models import Status, Task, Label
from tasks.filters import TaskFilter

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


class TestLabel(TestCase):
    fixtures = ['dbdump.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username='anton', password='asdf7jkl')

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
