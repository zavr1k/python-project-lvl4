from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django_filters.views import FilterView

from tasks.filters import TaskFilter
from tasks.forms import CreateTaskForm
from tasks.models import Task
from users.models import TaskUser


class Home(View):

    def get(self, request):
        content = {
            'title': _('Менеджер задач')
        }
        return render(request, 'tasks/main.html', content)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['title'] = _('Просмотр задачи')
        return context


class TaskList(LoginRequiredMixin, FilterView, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['title'] = _('Задачи')
        return context


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data(**kwargs)
        context['title'] = _('Создать задачу')
        context['button_text'] = _('Создать')
        return context

    def form_valid(self, form):
        form.instance.author = TaskUser.objects.get(id=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно создана'))
        return reverse_lazy('task_list')


class UpdateTask(LoginRequiredMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super(UpdateTask, self).get_context_data(**kwargs)
        context['title'] = _('Изменение задачи')
        context['button_text'] = _('Изменить')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно изменена'))
        return reverse_lazy('task_list')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteTask, self).get_context_data(**kwargs)
        context['title'] = _('Удаление задачи')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить задачу?')
        return context

    def dispatch(self, request, *args, **kwargs):
        task = self.model.objects.select_related('author').get(pk=kwargs['pk'])
        if task.author.pk != self.request.user.pk:
            messages.error(self.request,
                           _('Задачу может удалить только её автор'))
            return redirect('task_list')
        return super(DeleteTask, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("Задача успешно удалена"))
        return reverse_lazy('task_list')
