from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from tasks.models import Status, Task, Label
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')


class CreateStatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ('name',)
        labels = {
            'name': _('Имя')
        }


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
