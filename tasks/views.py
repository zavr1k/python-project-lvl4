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

from .forms import RegisterUserForm


class UserList(ListView):
    model = User
    template_name = 'tasks/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Users')
        return context


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'tasks/update_user.html'
    form_class = RegisterUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('User change')
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
    template_name = 'tasks/delete_user.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete user')
        return context

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.pk:
            messages.error(
                self.request,
                _("You are not allowed change other users"),
            )
            return redirect('user_list')
        return super(DeleteUser, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _("User successfully deleted"))
        return reverse_lazy('user_list')


class Home(View):

    def get(self, request):
        content = {
            'title': _('Task manager')
        }
        return render(request, 'tasks/main.html', content)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'tasks/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['title'] = _('Register')
        return context


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
