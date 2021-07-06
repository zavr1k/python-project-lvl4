from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterUserForm


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
