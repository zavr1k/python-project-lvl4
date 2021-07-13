from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from tasks.models import TaskStatus
from django.utils.translation import gettext_lazy as _


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')


class CreateStatusForm(ModelForm):

    class Meta:
        model = TaskStatus
        fields = ('title',)
        labels = {
            'title': _('Name')
        }
