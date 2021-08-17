import django_filters
from django import forms
from tasks.models import Label, Task


class TaskFilter(django_filters.FilterSet):

    @staticmethod
    def get_labels(self):
        return list((label.pk, label.name) for label in Label.objects.all(self))

    labels = django_filters.ChoiceFilter(field_name='labels', choices=get_labels)
    self_tasks = django_filters.BooleanFilter(field_name='author',
                                              widget=forms.CheckboxInput,
                                              method='get_self_tasks')

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'executor': ['exact'],
        }

    def get_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
