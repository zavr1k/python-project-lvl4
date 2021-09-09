from django.forms import ModelForm
from tasks.models import Task, Label
from django.utils.translation import gettext_lazy as _


class CreateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'executor': _('Исполнитель'),
            'status': _('Статус'),
            'labels': _('Метки')
        }


class CreateLabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ('name',)
        labels = {'name': _('Имя')}
