from django.contrib.auth.forms import UserCreationForm

from .models import TaskUser


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = TaskUser
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2',
                  )
