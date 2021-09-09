from django.contrib import admin

from tasks.models import Task, Label

admin.site.register(Task)
admin.site.register(Label)
