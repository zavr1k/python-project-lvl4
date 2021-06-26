from django.shortcuts import render
from django.utils.translation import gettext as _


def home(request):
    content = {
        'title': _('Task manager')
    }
    return render(request, 'tasks/main.html', content)
