from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import RegisterUserForm
from .models import TaskUser


class UserList(ListView):
    model = TaskUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Пользователи')
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'

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
    model = TaskUser
    template_name = 'users/register.html'
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
            return redirect('users')
        return super(UpdateUser, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно изменён'))
        return reverse_lazy('users')


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = TaskUser
    template_name = 'users/delete.html'

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
            return redirect('users')
        return super(DeleteUser, self).dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("Пользователь успешно удалён"))
        return reverse_lazy('users')
