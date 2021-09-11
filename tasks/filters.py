from django_filters import BooleanFilter, FilterSet
from django.forms import CheckboxInput
from tasks.models import Task


class TaskFilter(FilterSet):

    self_tasks = BooleanFilter(widget=CheckboxInput,
                               method='get_self_tasks')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def get_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
