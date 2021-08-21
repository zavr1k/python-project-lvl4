from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django_filters.views import FilterView

from tasks.filters import TaskFilter
from tasks.forms import RegisterUserForm, CreateStatusForm, \
    CreateTaskForm, CreateLabelForm
from tasks.models import Status, Task, Label


class Home(View):

    def get(self, request):
        content = {
            'title': _('Менеджер задач')
        }
        return render(request, 'tasks/main.html', content)


class UserList(ListView):
    model = User
    template_name = 'tasks/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Пользователи')
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'tasks/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = _('Регистрация')
        context['button_text'] = _('Зарегистрировать')
        return context

    def get_success_url(self):
        messages.success(
         self.request,
         _('Пользователь успешно зарегистрирован')
        )
        return reverse_lazy('login')


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'tasks/register.html'
    form_class = RegisterUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение пользователя')
        context['button_text'] = _('Изменить')
        return context

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            messages.error(
                self.request,
                _("У вас нет прав для изменения другого пользователя"),
            )
            return redirect('user_list')
        return super(UpdateUser, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно изменён'))
        return reverse_lazy('user_list')


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Удаление пользователя')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить пользователя?')
        return context

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            messages.error(
                self.request,
                _("У вас нет прав для изменения другого пользователя"),
            )
            return redirect('user_list')
        return super(DeleteUser, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("Пользователь успешно удален"))
        return reverse_lazy('user_list')


class LoginUser(LoginView):
    form = AuthenticationForm
    template_name = 'tasks/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = _('Вход')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Вы залогинены'))
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    messages.info(request, _('Вы разлогинены'))
    return redirect('main')


class StatusList(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'tasks/status_list.html'
    context_object_name = 'statuses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Статусы')
        return context


class CreateStatus(CreateView):
    form_class = CreateStatusForm
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Создать статус')
        context['button_text'] = _('Создать')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно создан'))
        return reverse_lazy('status_list')


class UpdateStatus(LoginRequiredMixin, UpdateView):
    form_class = CreateStatusForm
    template_name = 'tasks/create_form.html'
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение статуса')
        context['button_text'] = _('Изменить')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно изменен'))
        return reverse_lazy('status_list')


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Удаление статуса')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить статус?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно удален'))
        return reverse_lazy('status_list')


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
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data(**kwargs)
        context['title'] = _('Создать задачу')
        context['button_text'] = _('Создать')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно создана'))
        return reverse_lazy('task_list')


class UpdateTask(LoginRequiredMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_form.html'
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
    template_name = 'tasks/confirm_delete.html'

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
                           _('Задачу может удалить только ее автор'))
            return redirect('task_list')
        return super(DeleteTask, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("Задача успешно удалена"))
        return reverse_lazy('task_list')


class LabelList(LoginRequiredMixin, ListView):
    template_name = 'tasks/label_list.html'
    model = Label
    context_object_name = 'labels'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LabelList, self).get_context_data(**kwargs)
        context['title'] = _('Метки')
        return context


class CreateLabel(LoginRequiredMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Создать метку')
        context['button_text'] = _('Создать')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка создана'))
        return reverse_lazy('label_list')


class UpdateLabel(LoginRequiredMixin, UpdateView):
    form_class = CreateLabelForm
    template_name = 'tasks/create_form.html'
    model = Label

    def get_context_data(self, **kwargs):
        context = super(UpdateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Изменение метки')
        context['button_text'] = _('Изменить')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка изменена'))
        return reverse_lazy('label_list')


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteLabel, self).get_context_data(**kwargs)
        context['title'] = _('Удаление метки')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить метку?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка удалена'))
        return reverse_lazy('label_list')

    def dispatch(self, request, *args, **kwargs):
        labeled_tasks = Label.objects.get(pk=kwargs['pk']).tasks.all()
        if labeled_tasks:
            messages.error(
                self.request,
                _('Невозможно удалить метку, потому что она используется')
            )
            return redirect('label_list')
        return super(DeleteLabel, self).dispatch(self.request, *args, **kwargs)
