from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import CreateLabelForm
from .models import Label


class LabelList(LoginRequiredMixin, ListView):
    template_name = 'labels/label_list.html'
    model = Label
    context_object_name = 'labels'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LabelList, self).get_context_data(**kwargs)
        context['title'] = _('Метки')
        return context


class CreateLabel(LoginRequiredMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'

    def get_context_data(self, **kwargs):
        context = super(CreateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Создать метку')
        context['button_text'] = _('Создать')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно создана'))
        return reverse_lazy('label_list')


class UpdateLabel(LoginRequiredMixin, UpdateView):
    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'
    model = Label

    def get_context_data(self, **kwargs):
        context = super(UpdateLabel, self).get_context_data(**kwargs)
        context['title'] = _('Изменение метки')
        context['button_text'] = _('Изменить')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно изменена'))
        return reverse_lazy('label_list')


class DeleteLabel(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteLabel, self).get_context_data(**kwargs)
        context['title'] = _('Удаление метки')
        context['confirmation'] = \
            _('Вы уверены что хотите удалить метку?')
        return context

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно удалена'))
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
