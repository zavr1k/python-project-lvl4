from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import CreateStatusForm
from .models import Status


class StatusList(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Статусы')
        return context


class CreateStatus(CreateView):
    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'

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
    template_name = 'statuses/create_status.html'
    model = Status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменение статуса')
        context['button_text'] = _('Изменить')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно изменён'))
        return reverse_lazy('status_list')


class DeleteStatus(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Удаление статуса')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить статус?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно удалён'))
        return reverse_lazy('status_list')
