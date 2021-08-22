import django_filters
from django import forms
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):

    self_tasks = django_filters.BooleanFilter(field_name='author',
                                              widget=forms.CheckboxInput,
                                              method='get_self_tasks')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def get_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
