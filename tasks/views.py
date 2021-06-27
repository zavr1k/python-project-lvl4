from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View


class Home(View):

    def get(self, request):
        content = {
            'title': _('Task manager')
        }
        return render(request, 'tasks/main.html', content)
