from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=255,
                                 label=_('First name'),
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': _('First name')}))
    second_name = forms.CharField(max_length=255,
                                  label=_('Second name'),
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control',
                                      'placeholder': _('Second name')}))
    username = forms.CharField(max_length=255,
                               label=_('Username'),
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': _('Username')}))
    password1 = forms.CharField(max_length=50,
                                label=_('Password'),
                                min_length=3,
                                help_text='Пароль должен содержать '
                                          'минимум 8 символов',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Password')}))
    password2 = forms.CharField(max_length=50,
                                label=_('Password'),
                                min_length=3,
                                help_text='Для подтверждения введите, '
                                          'пожалуйста, пароль ещё раз.',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': _('Password confirmation')
                                }))

    class Meta:
        model = User
        fields = ('first_name',
                  'second_name',
                  'username',
                  'password1',
                  'password2')