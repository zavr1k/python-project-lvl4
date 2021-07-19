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
from django.contrib import messages

from tasks.forms import RegisterUserForm, CreateStatusForm, \
    CreateTaskForm, CreateLabelForm
from tasks.models import Status, Task, Label


class Home(View):

    def get(self, request):
        content = {
            'title': _('Task manager')
        }
        return render(request, 'tasks/main.html', content)


class UserList(ListView):
    model = User
    template_name = 'tasks/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Users')
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'tasks/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = _('Register')
        context['button_text'] = _('Register')
        return context


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'tasks/register.html'
    form_class = RegisterUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('User change')
        context['button_text'] = _('Update')
        return context

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            messages.error(
                self.request,
                _("You are not allowed change other users"),
            )
            return redirect('user_list')
        return super(UpdateUser, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _('User changed successfully'))
        return reverse_lazy('user_list')


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete user')
        context['confirmation'] = \
            _('Are you sure that you want to delete the user?')
        return context

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            messages.error(
                self.request,
                _("You are not allowed change other users"),
            )
            return redirect('user_list')
        return super(DeleteUser, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("User successfully deleted"))
        return reverse_lazy('user_list')


class LoginUser(LoginView):
    form = AuthenticationForm
    template_name = 'tasks/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = _('Authentication')
        return context

    def get_success_url(self):
        messages.success(self.request, _('You are logged in'))
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    messages.info(request, _('You are successfully logged out'))
    return redirect('main')


class StatusList(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'tasks/status_list.html'
    context_object_name = 'statuses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Statuses')
        return context


class CreateStatus(CreateView):
    form_class = CreateStatusForm
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        context['button_text'] = _('Create')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully created'))
        return reverse_lazy('status_list')


class UpdateStatus(LoginRequiredMixin, UpdateView):
    form_class = CreateStatusForm
    template_name = 'tasks/create_form.html'
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Change status')
        context['button_text'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully updated'))
        return reverse_lazy('status_list')


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete status')
        context['confirmation'] = \
            _('Are you sure that you want to delete the status?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Status successfully deleted'))
        return reverse_lazy('status_list')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['title'] = _('Tasks')
        return context


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data(**kwargs)
        context['title'] = _('Create task')
        context['button_text'] = _('Create')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('Task successfully created'))
        return reverse_lazy('task_list')


class UpdateTask(LoginRequiredMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = 'tasks/create_form.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super(UpdateTask, self).get_context_data(**kwargs)
        context['title'] = _('Update task')
        context['button_text'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Task successfully updated'))
        return reverse_lazy('task_list')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteTask, self).get_context_data(**kwargs)
        context['title'] = _('Delete task')
        context['confirmation'] = \
            _('Are you sure that you want to delete the task?')
        return context

    def dispatch(self, request, *args, **kwargs):
        task = self.model.objects.select_related('author').get(pk=kwargs['pk'])
        if task.author.pk != self.request.user.pk:
            messages.error(self.request,
                           _('Only the author can delete tasks'))
            return redirect('task_list')
        return super(DeleteTask, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("Task successfully deleted"))
        return reverse_lazy('task_list')


class LabelList(LoginRequiredMixin, ListView):
    template_name = 'tasks/label_list.html'
    model = Label
    context_object_name = 'labels'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LabelList, self).get_context_data(**kwargs)
        context['title'] = _('Labels')
        return context


class CreateLabel(LoginRequiredMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'tasks/create_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Create label')
        context['button_text'] = _('Create')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label created'))
        return reverse_lazy('label_list')


class UpdateLabel(LoginRequiredMixin, UpdateView):
    form_class = CreateLabelForm
    template_name = 'tasks/create_form.html'
    model = Label

    def get_context_data(self, **kwargs):
        context = super(UpdateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Update label')
        context['button_text'] = _('Update')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label was updated'))
        return reverse_lazy('label_list')


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'tasks/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteLabel, self).get_context_data(**kwargs)
        context['title'] = _('Delete label')
        context['confirmation'] = \
            _('Are you sure that you want to delete the label?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Label successfully deleted'))
        return reverse_lazy('label_list')

    def dispatch(self, request, *args, **kwargs):
        labeled_tasks = Label.objects.get(pk=kwargs['pk']).tasks.all()
        if labeled_tasks:
            messages.error(
                self.request,
                _('Cannot remove a label because it is in use')
            )
            return redirect('label_list')
        return super(DeleteLabel, self).dispatch(self.request, *args, **kwargs)
