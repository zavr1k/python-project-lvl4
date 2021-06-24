from django.shortcuts import render
from task_manager.settings import STATIC_ROOT


def home(request):
    return render(request, 'tasks/main.html', {'sr': STATIC_ROOT})
