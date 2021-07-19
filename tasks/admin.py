from django.contrib import admin

from tasks.models import Task, Status, Label

admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Label)
